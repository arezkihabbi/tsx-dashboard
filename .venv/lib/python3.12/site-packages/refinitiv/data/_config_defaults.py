import hashlib
import warnings

from refinitiv.data._external_libraries.python_configuration import config_from_dict

__all__ = ("config",)

data = {
    "config-change-notifications-enabled": False,
    "raise_exception_on_error": True,
    "http": {
        "max-connections": 100,
        "max-keepalive-connections": 20,
        "request-timeout": 20,
        "auto-retry": {"number-of-retries": 6, "on-errors": [429], "backoff-factor": 1},
    },
    "logs": {
        "level": "info",
        "filter": "*",
        "transports": {
            "console": {"enabled": False, "colorize": False},
            "file": {
                "enabled": False,
                "name": "refinitiv-data-lib.log",
                "size": "10M",
                "interval": "1d",
                "maxFiles": 10,
            },
        },
    },
    "usage_logger": {
        "enabled": False,
    },
    "sessions": {
        "default": "desktop.workspace",
        "platform": {
            "default": {
                "signon_control": True,
                "auto-reconnect": True,
                "server-mode": False,
                "verify_scope": True,
                "base-url": "https://api.refinitiv.com",
                "auth": {
                    "revoke": "/auth/oauth2/v1/revoke",
                    "v1": {"url": "/auth/oauth2/v1", "authorize": "/authorize", "token": "/token"},
                    "v2": {"url": "/auth/oauth2/v2", "token": "/token"},
                },
            }
        },
        "desktop": {
            "workspace": {
                "app-key": "DEFAULT_WORKSPACE_APP_KEY",
                "base-url": "http://localhost:9000",
                "platform-paths": {"rdp": "/api/rdp", "udf": "/api/udf"},
                "handshake-url": "/api/handshake",
            },
        },
    },
    "apis": {
        "file-store": {
            "url": "/file-store/v1",
            "endpoints": {
                "buckets": "/buckets",
                "file-sets": "/file-sets",
                "files": "/files",
                "packages": "/packages",
            },
        },
        "data": {
            "historical-pricing": {
                "url": "/data/historical-pricing/v1",
                "endpoints": {
                    "events": "/views/events",
                    "interday-summaries": "/views/interday-summaries",
                    "intraday-summaries": "/views/intraday-summaries",
                },
            },
            "pricing": {
                "url": "/data/pricing",
                "endpoints": {"snapshots": "/snapshots/v1/", "chains": "/chains/v1/"},
            },
            "quantitative-analytics-dates-and-calendars": {
                "url": "/data/quantitative-analytics-dates-and-calendars/v1",
                "endpoints": {
                    "add-periods": {"sync": "/add-periods"},
                    "holidays": {"sync": "/holidays"},
                    "count-periods": {"sync": "/count-periods"},
                    "date-schedule": {"sync": "/date-schedule"},
                    "is-working-day": {"sync": "/is-working-day"},
                },
            },
            "quantitative-analytics-financial-contracts": {
                "url": "/data/quantitative-analytics/v1",
                "endpoints": {
                    "financial-contracts": {
                        "sync": "/financial-contracts",
                        "async": "/async-financial-contracts",
                    },
                    "async-operation": "/async-operation",
                    "async-resource": "/async-resource",
                },
                "auto-retry": True,
            },
            "quantitative-analytics-curves-and-surfaces": {
                "url": "/data/quantitative-analytics-curves-and-surfaces/v1",
                "endpoints": {
                    "bond-curves": {
                        "curves": "/curves/bond-curves/curves",
                    },
                    "cross-currency-curves": {
                        "curves": "/curves/cross-currency-curves/curves",
                        "definitions": {
                            "create": "/curves/cross-currency-curves/definitions/create",
                            "delete": "/curves/cross-currency-curves/definitions/delete",
                            "get": "/curves/cross-currency-curves/definitions/get",
                            "search": "/curves/cross-currency-curves/definitions/search",
                            "update": "/curves/cross-currency-curves/definitions/update",
                        },
                        "triangulate-definitions": {
                            "search": "/curves/cross-currency-curves/triangulate-definitions/search"
                        },
                    },
                    "forward-curves": "/curves/forward-curves",
                    "surfaces": {"sync": "/surfaces", "async": "/async-surfaces"},
                    "zc-curves": "/curves/zc-curves",
                    "zc-curve-definitions": "/curves/zc-curve-definitions",
                    "async-operation": "/async-operation",
                    "async-resource": "/async-resource",
                },
                "auto-retry": True,
            },
            "news": {
                "url": "/data/news/v1",
                "endpoints": {
                    "headlines": "/headlines",
                    "stories": "/stories",
                    "top-news": "/top-news",
                    "images": "/images",
                    "online-reports": "/online-reports",
                },
            },
            "environmental-social-governance": {
                "url": "/data/environmental-social-governance/v1",
                "endpoints": {
                    "universe": "/universe",
                    "basic": "/views/basic",
                    "measures-full": "/views/measures-full",
                    "measures-standard": "/views/measures-standard",
                    "scores-full": "/views/scores-full",
                    "scores-standard": "/views/scores-standard",
                },
            },
            "datagrid": {
                "url": "/data/datagrid/beta1",
                "underlying-platform": "udf",
                "endpoints": {"standard": "/"},
            },
            "ownership": {
                "url": "/data/ownership/v1",
                "endpoints": {
                    "consolidated": {
                        "breakdown": "/views/consolidated/breakdown",
                        "concentration": "/views/consolidated/concentration",
                        "investors": "/views/consolidated/investors",
                        "recent-activity": "/views/consolidated/recent-activity",
                        "shareholders-history-report": "/views/consolidated/shareholders-history-report",
                        "shareholders-report": "/views/consolidated/shareholders-report",
                        "top-n-concentration": "/views/consolidated/top-n-concentration",
                    },
                    "fund": {
                        "breakdown": "/views/fund/breakdown",
                        "concentration": "/views/fund/concentration",
                        "investors": "/views/fund/investors",
                        "holdings": "/views/fund/holdings",
                        "recent-activity": "/views/fund/recent-activity",
                        "shareholders-history-report": "/views/fund/shareholders-history-report",
                        "shareholders-report": "/views/fund/shareholders-report",
                        "top-n-concentration": "/views/fund/top-n-concentration",
                    },
                    "insider": {
                        "shareholders-report": "/views/insider/shareholders-report",
                        "transaction-report": "/views/insider/transaction-report",
                    },
                    "investor": {"holdings": "/views/investor/holdings"},
                    "org-info": "/views/org-info",
                },
            },
            "estimates": {
                "url": "/data/estimates/v1",
                "endpoints": {
                    "view-actuals": {
                        "annual": "/view-actuals/annual",
                        "interim": "/view-actuals/interim",
                    },
                    "view-actuals-kpi": {
                        "annual": "/view-actuals-kpi/annual",
                        "interim": "/view-actuals-kpi/interim",
                    },
                    "view-summary": {
                        "annual": "/view-summary/annual",
                        "historical-snapshots-non-periodic-measures": "/view-summary/historical-snapshots-non-periodic-measures",
                        "historical-snapshots-periodic-measures-annual": "/view-summary/historical-snapshots-periodic-measures-annual",
                        "historical-snapshots-periodic-measures-interim": "/view-summary/historical-snapshots-periodic-measures-interim",
                        "historical-snapshots-recommendations": "/view-summary/historical-snapshots-recommendations",
                        "interim": "/view-summary/interim",
                        "non-periodic-measures": "/view-summary/non-periodic-measures",
                        "recommendations": "/view-summary/recommendations",
                    },
                    "view-summary-kpi": {
                        "annual": "/view-summary-kpi/annual",
                        "historical-snapshots-kpi": "/view-summary-kpi/historical-snapshots-kpi",
                        "interim": "/view-summary-kpi/interim",
                    },
                },
            },
            "custom-instruments": {
                "url": "/data/custom-instruments/v1",
                "endpoints": {
                    "instruments": "/instruments",
                    "search": "/search",
                    "events": "/events",
                    "interday-summaries": "/interday-summaries",
                    "intraday-summaries": "/intraday-summaries",
                },
            },
            "filings": {
                "headers": {
                    "ClientID": "API_Playground",
                    "X-Api-Key": "155d9dbf-f0ac-46d9-8b77-f7f6dcd238f8",
                    "Accept": "*/*",
                },
                "url": "/data/filings/v1",
                "endpoints": {"retrieval": "/retrieval"},
            },
        },
        "discovery": {
            "search": {
                "url": "/discovery/search/v1/",
                "endpoints": {
                    "search": "/",
                    "lookup": "/lookup",
                    "metadata": "/metadata/views",
                },
            }
        },
        "streaming": {
            "pricing": {
                "url": "/streaming/pricing/v1",
                "endpoints": {
                    "main": {
                        "contrib": {"field-validation": False},
                        "metadata": {"download": False},
                        "path": "/",
                        "protocols": ["OMM"],
                        "locations": [],
                    }
                },
            },
            "custom-instruments": {
                "url": "/streaming/custom-instruments/v1",
                "endpoints": {
                    "resource": {
                        "path": "/resource",
                        "protocols": ["OMM"],
                        "locations": [],
                    }
                },
            },
            "trading-analytics": {
                "url": "/streaming/trading-analytics/trade-data/beta1",
                "endpoints": {
                    "redi": {
                        "path": "/redi",
                        "protocols": ["OMM", "RDP"],
                        "locations": [],
                    }
                },
            },
            "quantitative-analytics": {
                "url": "/streaming/quantitative-analytics/beta1",
                "endpoints": {
                    "financial-contracts": {
                        "path": "/financial-contracts",
                        "protocols": ["OMM", "RDP"],
                        "locations": [],
                    }
                },
            },
            "benchmark": {
                "url": "/streaming/benchmark/v1",
                "endpoints": {
                    "resource": {
                        "path": "/resource",
                        "protocols": ["RDP"],
                        "locations": [],
                    }
                },
            },
        },
        "data-store": {"url": "/data-store/v1", "endpoints": {"graphql": "/graphql"}},
    },
    "bulk": {
        "esg": {
            "standard_scores": {
                "package": {
                    "bucket": "bulk-ESG",
                    "name": "Bulk-ESG-Global-Scores-Wealth-Standard-v1",
                    "download": {
                        "path": "./downloads/esg/standard_scores",
                        "auto-retry": {"enabled": True, "count": 3},
                        "auto-extract": True,
                    },
                },
                "db": {
                    "connection": {
                        "module": "mysql",
                        "parameters": {
                            "user": "",
                            "password": "",
                            "host": "",
                            "port": 3306,
                            "database": "",
                        },
                    },
                    "table-auto-creation": True,
                    "create-table-queries": [
                        {
                            "table-name": "MY_STANDARD_SCORES_TABLE",
                            "create-query": "CREATE TABLE IF NOT EXISTS MY_STANDARD_SCORES_TABLE(ORGANIZATION varchar(255),INSERT_DATE varchar(255), INSTRUMENT varchar(255), PERIOD_END_DATE varchar(255), ESG_C_SCORE varchar(255),ESG_SCORE varchar(255),ENVIRONMENT_PILLAR_SCORE varchar(255), SOCIAL_PILLAR_SCORE varchar(255), GOVERNANCE_PILLAR_SCORE varchar(255), CONSTRAINT UC_MY_STANDARD_SCORES UNIQUE (INSTRUMENT,PERIOD_END_DATE))",
                            "check-if-exists-query": "SHOW TABLES",
                        }
                    ],
                    "search-query": "SELECT * FROM MY_STANDARD_SCORES_TABLE WHERE INSTRUMENT IN #{universe}",
                    "insert-queries": [
                        "REPLACE INTO MY_STANDARD_SCORES_TABLE(ORGANIZATION, INSERT_DATE, INSTRUMENT, PERIOD_END_DATE, ESG_C_SCORE, ESG_SCORE, ENVIRONMENT_PILLAR_SCORE, SOCIAL_PILLAR_SCORE, GOVERNANCE_PILLAR_SCORE) VALUES ('#{Fields.ESGOrganization.Names.Name.OrganizationName.0.OrganizationNormalizedName}', '#{File.DateTime}', '#{Fields.StatementDetails.OrganizationId}', '#{Fields.StatementDetails.FinancialPeriodEndDate}', '#{Fields.ESGScores.ESGCombinedScore.Value}', '#{Fields.ESGScores.ESGScore.Value}', '#{Fields.ESGScores.EnvironmentPillarScore.Value}', '#{Fields.ESGScores.SocialPillarScore.Value}', '#{Fields.ESGScores.GovernancePillarScore.Value}')"
                    ],
                    "stop-on-error": False,
                    "clean-up-queries": ["DELETE FROM MY_STANDARD_SCORES_TABLE"],
                    "output-fields-mapping": {
                        "INSTRUMENT": "instrument",
                        "PERIOD_END_DATE": "periodenddate",
                        "ESG_C_SCORE": "TR.TRESGCScore",
                        "ESG_SCORE": "TR.TRESGScore",
                        "ENVIRONMENT_PILLAR_SCORE": "TR.EnvironmentPillarScore",
                        "SOCIAL_PILLAR_SCORE": "TR.SocialPillarScore",
                        "GOVERNANCE_PILLAR_SCORE": "TR.GovernancePillarScore",
                    },
                },
            },
        },
    },
}

current_checksum = hashlib.md5(repr(data).encode()).hexdigest()  # NOSONAR
fixed_checksum = "505794edc4a95d01504db1911e451d68"

if current_checksum != fixed_checksum:
    warnings.warn(
        "Default library config was changed. This may cause unexpected errors. "
        "Please use user config to introduce new changes. You can reinstall "
        "refinitiv-data to revert changes back."
    )

config = config_from_dict(data)

# Run this module as script to update checksum after defaults change
if __name__ == "__main__":
    # Used only as a script to get new checksum
    print("current checksum: ", current_checksum)  # pylint: disable=no-print-statement
