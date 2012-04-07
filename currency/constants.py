ALERT_TIME =                    {       "cfi": 30,
                                        "medical": 30,
                                        "landing": 10,
                                        "fr": 30,
                                }

EXPIRE_MONTHS =                 {       "faa_fr": 24,
                                        "faa_cfi": 24,
                                        "faa_landing": 90
                                }

FAA_MEDICAL_DURATIONS =         {                               #the time elapsed from the original exam date for each downgrade
                                        "over": (6, 12, 48),
                                        "under": (12, 12, 60)
                                }

CURRENCY_TITLES =               {       "fr": "Flight Review",
                                        "cfi": "Instructor Renewal",
                                        0: "Medical Certificate",
                                        1: "1st Class Medical",
                                        2: "2nd Class Medical",
                                        3: "3rd Class Medical"
                                }

FAA_MEDICAL_DURATIONS = {                               #the time elapsed from the original exam date for each downgrade in calendar months
                                        "over": (6, 12, 48),
                                        "under": (12, 12, 60)
                                }


CURRENCY_DATA =
    {   0:      ("","",""),
                        1:      ("Flight Instructor",   "24", "cm", "30", "d"), # (name, duration, duration units, alert time, alert time units)
                        2:      ("Flight Review",       "24", "cm", "30", "d"),
                        3:      ("1st Class Medical"),
                        4:      ("2nd Class Medical"),
                        5:      ("3rd Class Medical"),

                        100:    ("FAA Landings",        "90", "d", "10", "d"),
                }
