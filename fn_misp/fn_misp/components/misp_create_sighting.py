# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
"""Function implementation"""

import logging
from pymisp import PyMISP
import time
from resilient_circuits import ResilientComponent, function, StatusMessage, FunctionResult, FunctionError


class FunctionComponent(ResilientComponent):
    """Component that implements Resilient function(s)"""

    def __init__(self, opts):
        """constructor provides access to the configuration options"""
        super(FunctionComponent, self).__init__(opts)
        self.options = opts.get("fn_misp", {})

    @function("misp_create_sighting")
    def _misp_create_sighting_function(self, event, *args, **kwargs):
        """Function: """
        try:

            def get_config_option(option_name, optional=False):
                """Given option_name, checks if it is in app.config. Raises ValueError if a mandatory option is missing"""
                option = self.options.get(option_name)

                if option is None and optional is False:
                    err = "'{0}' is mandatory and is not set in ~/.resilient/app.config file. You must set this value to run this function".format(option_name)
                    raise ValueError(err)
                else:
                    return option

            API_KEY = get_config_option("misp_key")
            URL = get_config_option("misp_url")
            VERIFY_CERT = True if get_config_option("verify_cert").lower() == "true" else False

            # Get the function parameters:
            misp_sighting = kwargs.get("misp_sighting")  # text

            log = logging.getLogger(__name__)
            log.info("misp_sighting: %s", misp_sighting)

            misp_client = PyMISP(URL, API_KEY, VERIFY_CERT, 'json')

            sighting_json = {
                            "values":["{}".format(misp_sighting)], 
                            "timestamp": int(time.time())
                            }

            result = misp_client.set_sightings(sighting_json)

            results = { "success": True,
                        "content": result }

            # Produce a FunctionResult with the results
            yield FunctionResult(results)
        except Exception:
            yield FunctionError()
