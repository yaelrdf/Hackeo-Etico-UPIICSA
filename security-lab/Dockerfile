FROM kalilinux/kali-rolling:latest

# Update package lists and install network tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    net-tools \
    iputils-ping \
    dnsutils \
    traceroute \
    whois \
    git \
    sudo \
    kali-linux-headless \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash kali && \
    usermod -aG sudo kali && \
    echo "kali ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set the default user
USER kali
WORKDIR /home/kali

# Keep container running
CMD ["/bin/bash", "-c", "sleep infinity"]
