# Use Alpine as base image
# Use Ubuntu as the base image
FROM ubuntu:latest

ENV USER=runner
ENV PASSWORD=password_
ENV GROUP=$USER
ENV UID=1001
ENV GID=1001
ENV WORK_DIR=/home/${USER}/actions_runner
ENV RUNNER_URL="https://github.com/actions/runner/releases/download/v2.316.1/actions-runner-linux-x64-2.316.1.tar.gz"
ENV PROJECT_NAME=''
ENV TOKEN=''

# Install necessary tools
RUN apt-get update && \
    apt-get install -y tar curl sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p $WORK_DIR

WORKDIR $WORK_DIR
RUN curl -o runner.tar.gz -L ${RUNNER_URL} && \
    tar zxvf runner.tar.gz
#    ./bin/installdependencies.sh

# Create a non-root user in the container
#RUN groupadd -g ${GID} ${GROUP}
#RUN useradd -u ${UID} -g ${GID} -m -s /bin/bash ${USER}
#RUN echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to the non-root user
#USER $USER

#RUN ./config.sh --url https://github.com/RTKmoko/${PROJECT_NAME} --token ${TOKEN}

#ENTRYPOINT ["./run.sh" ]
ENTRYPOINT ["/bin/bash" ]


# Create a folder
#$ mkdir actions-runner && cd actions-runner# Download the latest runner package
#$ curl -o actions-runner-linux-x64-2.316.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.316.1/actions-runner-linux-x64-2.316.1.tar.gz
#Copied!# Optional: Validate the hash
#$ echo "d62de2400eeeacd195db91e2ff011bfb646cd5d85545e81d8f78c436183e09a8  actions-runner-linux-x64-2.316.1.tar.gz" | shasum -a 256 -c# Extract the installer
#$ tar xzf ./actions-runner-linux-x64-2.316.1.tar.gz
# Create the runner and start the configuration experience
#$ ./config.sh --url https://github.com/RTKmoko/3D-polymer-solubility-calculator --token ACUUWCZXAGKWEQQFJU3ZKCLGL5PSW
# Last step, run it!
#$ ./run.sh
