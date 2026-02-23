template = {
    'dns': {},
    'inbounds':
        [
            {
                'listen': '0.0.0.0',
                'port': 1080,
                'protocol': 'socks',
                'settings': {
                    'auth': 'noauth',
                    'udp': True
                }
            },
            {
                'listen': '0.0.0.0',
                'port': 8080,
                'protocol': 'http',
                'settings': {'timeout': 300}
            }
        ],
    'log':
        {
            'access': '/dev/stdout',
            'error': '/dev/stderr',
            'loglevel': 'warning'
        },
    'outbounds':
        [
            {
                'protocol': 'vmess',
                'settings':
                    {
                        'vnext':
                            [
                                {
                                    'address': 'proxy-server.com',
                                    'port': 443,
                                    'users':
                                        [
                                            {
                                                'id': '657cd87b-9c0a-4399-afdc-1ccc7091972d'
                                            }
                                        ]
                                }
                            ]
                    },
                'streamSettings':
                    {
                        'network': 'ws',
                        'security': 'tls',
                        'tlsSettings':
                            {
                                'serverName': 'www.baidu.com'
                            },
                        'wsSettings':
                            {
                                'path': '/v2ray'
                            }
                    },
                'tag': 'proxy'
            },
            {
                'protocol': 'freedom',
                'settings': {},
                'tag': 'direct'
            },
            {
                'protocol': 'blackhole',
                'settings': {},
                'tag': 'blocked'}
        ],
    'routing':
        {
            'domainStrategy': 'AsIs',
            'rules':
                [
                    {
                        'domain': ['geosite:cn'],
                        'outboundTag': 'direct',
                        'type': 'field'
                    },
                    {
                        'domain': ['geosite:category-ads-all'],
                        'outboundTag': 'blocked',
                        'type': 'field'
                    },
                    {
                        'domain': ['geosite:google', 'geosite:facebook'],
                        'outboundTag': 'proxy',
                        'type': 'field'
                    },
                    {
                        'ip': ['geoip:private'],
                        'outboundTag': 'blocked',
                        'type': 'field'
                    }
                ]
        }
}

ws_template = {
    'protocol': 'vmess',
    'settings':
        {
            'vnext':
                [
                    {
                        'address': 'proxy-server.com',
                        'port': 443,
                        'users':
                            [
                                {
                                    'id': '657cd87b-9c0a-4399-afdc-1ccc7091972d',
                                    "alterId": 4,
                                    "security": "auto"
                                }
                            ]
                    }
                ]
        },
    'streamSettings':
        {
            'network': 'ws',
            'security': 'tls',
            'tlsSettings':
                {
                    'serverName': 'www.baidu.com'
                },
            'wsSettings':
                {
                    'path': '/v2ray'
                }
        },
    'tag': 'proxy'
}

tcp_template = {
    "protocol": "vmess",
    "settings": {
        "vnext": [
            {
                "address": "proxy-server.com",
                "port": 12345,
                "users": [
                    {
                        "id": "657cd87b-9c0a-4399-afdc-1ccc7091972d",
                        "alterId": 4,
                        "security": "auto"
                    }
                ]
            }
        ]
    },
    "tag": "proxy",
    "streamSettings": {
        "network": "tcp",
        "security": "tls"
    }
}
