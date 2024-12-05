# -*- coding: utf-8 -*-

from erp_mpro import __version__


def sige_version(request):
    return {'versao': __version__}
