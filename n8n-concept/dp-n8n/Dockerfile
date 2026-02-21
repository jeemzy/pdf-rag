# Custom n8n image with additional community nodes
FROM docker.n8n.io/n8nio/n8n

# Switch to root to install npm packages
USER root

# Install the semantic splitter with context node
RUN cd /usr/local/lib/node_modules/n8n && \
    npm install n8n-nodes-semantic-splitter-with-context

# Switch back to node user
USER node

