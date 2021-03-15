"""DSM Certificate data."""

import json


class SynoCoreCertificate:
    """Class containing Certificate data."""

    API_CERTIFICATE_KEY = "SYNO.Core.Certificate.CRT"
    API_CERTIFICATE_SERVICE_KEY = "SYNO.Core.Certificate.Service"  # method='set'

    def __init__(self, dsm):
        """Constructor method."""
        self._dsm = dsm
        self._data = {}

    def update(self):
        """Updates certificate data."""
        raw_data = self._dsm.get(self.API_CERTIFICATE_KEY, "list")
        if raw_data:
            self._data = raw_data["data"]

    @property
    def success(self):
        """Gets the last scan success."""
        return self._data.get("success")

    @property
    def all(self):
        """Gets all certificate names."""
        cert_list = self._data.get("certificates")
        return [cert['desc'] for cert in cert_list]

    @property
    def self_signed(self):
        """Gets only self-signed certificate names."""
        cert_list = self._data.get("certificates")
        return [cert['desc'] for cert in cert_list if cert['issuer']['organization'] == 'Synology Inc.']

    @property
    def lets_encrypt(self):
        """Gets only Let's Encrypt certificate names."""
        cert_list = self._data.get("certificates")
        return [cert['desc'] for cert in cert_list if cert['issuer']['organization'] == "Let's Encrypt"]

    def _services_by_certificate(self, cert_name):
        """Gets services associated with certificate `cert_name`"""
        cert_list = self._data.get("certificates")
        cert_list = [cert for cert in cert_list if cert['desc'] == cert_name]
        if not cert_list:
            return []
        cert = cert_list[0]
        services = [serv for serv in cert['services']]
        return services

    def services_by_certificate(self, cert_name):
        services = [svc['service']
                    for svc in self._services_by_certificate(cert_name)]
        return services or []

    def _services(self):
        """Gets all services that can be associated with certificates"""
        services = []
        for cert in self.all:
            services += self._services_by_certificate(cert)
        return services

    def services(self):
        services = [svc['service'] for svc in self._services()]
        return services or []

    def _get_cert_id_by_cert_name(self, cert_name):
        cert_id = [cert['id'] for cert in self._data.get(
            "certificates") if cert['desc'] == cert_name]
        if len(cert_id) != 1:
            raise RuntimeError('Certificate not found')
        return cert_id[0]

    def _get_cert_id_by_service_name(self, service_name):
        for cert in self._data.get('certificates'):
            for svc in cert['services']:
                if svc['service'] == service_name:
                    return cert['id']
        raise RuntimeError(
            'No certificate was found associated to the specified service')

    def assign_certificate_to_service(self, cert_name, service_names):
        """Sets certificate `cert_name` to all `service_name` services"""

        # Verify specified cert_name is valid
        if cert_name is None or cert_name not in self.all:
            raise RuntimeError('Invalid certificate name!')

        # Verify specified services are valid
        all_services = self.services()
        valid_services = [svc for svc in service_names if svc in all_services]
        if not valid_services:
            raise RuntimeError('Invalid service(s) name(s)!')

        # Prepare payload for the REST API
        new_cert_id = self._get_cert_id_by_cert_name(cert_name)
        services = self._services()
        services = [{'service': svc, 'old_id': self._get_cert_id_by_service_name(svc['service']), 'id': new_cert_id, }
                    for svc in services if svc['service'] in valid_services]
        params = {'settings': json.dumps(services)}

        # Final validation
        for svc in services:
            if not svc['service'] or not svc['old_id'] or not svc['id']:
                raise RuntimeError('Malformed service configuration!')
            if svc['old_id'] == svc['id']:
                raise RuntimeError('Service {} is already using the specified certificate'. format(
                    svc['service']['display_name']))

        # REST API call
        res = self._dsm.post(api=self.API_CERTIFICATE_SERVICE_KEY,
                             method="set",
                             params=params)

        return res
