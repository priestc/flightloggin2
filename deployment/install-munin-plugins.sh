#!/bin/bash
ln -s /usr/share/munin/plugins/postgres_bgwriter /etc/munin/plugins/postgres_bgwriter
ln -s /usr/share/munin/plugins/postgres_cache_ /etc/munin/plugins/postgres_cache_logbook
ln -s /usr/share/munin/plugins/postgres_connections_ /etc/munin/plugins/postgres_connections_logbook
ln -s /usr/share/munin/plugins/postgres_locks_ /etc/munin/plugins/postgres_locks_logbook
ln -s /usr/share/munin/plugins/postgres_querylength_ /etc/munin/plugins/postgres_querylength_logbook
ln -s /usr/share/munin/plugins/postgres_scans_ /etc/munin/plugins/postgres_scans_logbook
ln -s /usr/share/munin/plugins/postgres_size_ /etc/munin/plugins/postgres_size_logbook
ln -s /usr/share/munin/plugins/postgres_transactions_ /etc/munin/plugins/postgres_transactions_logbook
ln -s /usr/share/munin/plugins/postgres_xlog /etc/munin/plugins/postgres_xlog