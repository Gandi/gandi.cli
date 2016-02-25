""" Hosted certificate commands module. """

import os
from gandi.cli.core.base import GandiModule


class HostedCert(GandiModule):
    """ Module to handle CLI commands.

    $ gandi certstore list
    $ gandi certstore info
    $ gandi certstore create
    $ gandi certstore delete
    """

    @classmethod
    def from_fqdn(cls, fqdn):
        return cls.list({'fqdns': '%s' % fqdn, 'state': 'created'})

    @classmethod
    def usable_id(cls, id):
        """ Retrieve id from single input. """
        hcs = cls.from_fqdn(id)
        if hcs:
            return [hc_['id'] for hc_ in hcs]

        try:
            return int(id)
        except (TypeError, ValueError):
            pass

    @classmethod
    def list(cls, options=None):
        """ List hosted certificates. """
        options = options or {}
        return cls.call('cert.hosted.list', options)

    @classmethod
    def info(cls, id):
        """ Display information about a hosted certificate. """
        return cls.call('cert.hosted.info', id)

    @classmethod
    def infos(cls, fqdn):
        """ Display information about hosted certificates for a fqdn. """
        if isinstance(fqdn, (list, tuple)):
            ids = []
            for fqd_ in fqdn:
                ids.extend(cls.infos(fqd_))
            return ids

        ids = cls.usable_id(fqdn)
        if not ids:
            return []

        if not isinstance(ids, (list, tuple)):
            ids = [ids]

        return [cls.info(id_) for id_ in ids]

    @classmethod
    def create(cls, key, crt):
        """ Add a new crt in the hosted cert store. """
        options = {'crt': crt, 'key': key}
        return cls.call('cert.hosted.create', options)

    @classmethod
    def delete(cls, id_):
        """ Remove a cert from the hosted cert store. """
        return cls.call('cert.hosted.delete', id_)

    @classmethod
    def activate_ssl(cls, vhosts, ssl, private_key, poll_cert):
        from .cert import Certificate
        if not ssl:
            return True

        if not isinstance(vhosts, (list, tuple)):
            vhosts = [vhosts]

        missing = []
        for vhost in vhosts:
            try:
                hostedcert = cls.infos(vhost)
                if hostedcert:
                    cls.debug('There is a cert in store for %s' % vhost)
                else:
                    missing.append(vhost)
            except ValueError:
                missing.append(vhost)

        if not missing:
            return True

        vhosts = missing
        cls.debug('Trying to get certificate or generate it for %s' %
                  (', '.join(vhosts)))
        vhost = vhosts[0]
        altnames = vhosts[1:]
        cert = Certificate.get_latest_valid(vhosts)
        if cert:
            if not private_key:
                cls.echo('Please give the private key for certificate id %s '
                         '(CN: %s)' % (cert['id'], cert['cn']))
                return False

            cls.echo('Will use the certificate id %s (CN: %s)' %
                     (cert['id'], cert['cn']))

            if os.path.isfile(private_key):
                with open(private_key) as fhandle:
                    private_key = fhandle.read()

            crt = Certificate.pretty_format_cert(cert)
            cls.create(private_key, crt)
        elif poll_cert:
            cls.echo('This operation will take a long time waiting for the '
                     'certificate to be generated.')

            # create the certificate
            csr = Certificate.process_csr(vhost, private_key=private_key)
            package = Certificate.get_package(vhost, altnames=altnames)
            oper = Certificate.create(csr, 1, package, altnames=altnames)

            cls.echo('If the term close, you can check the certificate create '
                     'operation with :')
            cls.echo('$ gandi certificate follow %s' % oper['id'])
            cls.echo("And when it's DONE you can continue doing :")
            cls.echo('$ gandi certificate export %s' % vhost)
            cls.echo('$ gandi certstore create --private-key %s --certificate '
                     '%s' % (vhost.replace('*.', 'wildcard.') + '.key',
                             vhost.replace('*.', 'wildcard.') + '.crt'))
            cls.echo('And then relaunch the current command.\n')
            cls.echo('Creating the certificate for %s%s' %
                     (vhost,
                      ' (%s)' % ', '.join(altnames) if altnames else ''))
            cls.display_progress(oper)

            # create the hosted certificate.
            # this will always give us a file name.
            _, private_key = Certificate.gen_pk(vhost, private_key)

            with open(private_key) as fhandle:
                private_key = fhandle.read()

            cert = Certificate.get_latest_valid(vhosts)
            crt = Certificate.pretty_format_cert(cert)
            cls.create(private_key, crt)
        else:
            cls.echo('There is no certificate for %s.' % ', '.join(vhosts))
            cls.echo('Create the certificate with (for exemple) :')
            cls.echo('$ gandi certificate create --cn %s --type std %s' %
                     (vhost, '--altnames=%s' % ','.join(altnames) if altnames
                      else ''))
            cls.echo('Or relaunch the current command with --poll-cert option')
        return True
