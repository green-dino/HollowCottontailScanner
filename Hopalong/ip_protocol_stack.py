network_layers = {
    "application": {
        "description": "supporting network applications",
        "protocols": ["FTP", "SMTP", "HTTP"]
    },
    "transport": {
        "description": "process-process data transfer",
        "protocols": ["TCP", "UDP"]
    },
    "network": {
        "description": "routing of datagrams from source to destination",
        "protocols": ["IP", "routing protocols"]
    },
    "link": {
        "description": "data transfer between neighboring network elements",
        "protocols": ["Ethernet", "802.11 (WiFi)", "PPP"]
    },
    "physical": {
        "description": "bits 'on the wire'",
        "protocols": []
    }
}