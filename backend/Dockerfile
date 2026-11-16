FROM cgr.dev/chainguard/wolfi-base:latest@sha256:2c12da5496e21e99003b3db3b9246f025e53d533c4df334205391260f1e8f85b AS builder

ARG INSTALL_SOURCE
ARG PYTHON_VERSION

# skipcq: DOK-DL3018
RUN apk add --no-cache build-base git uv

USER nonroot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv tool install ${INSTALL_SOURCE} --python ${PYTHON_VERSION}

FROM cgr.dev/chainguard/wolfi-base:latest@sha256:2c12da5496e21e99003b3db3b9246f025e53d533c4df334205391260f1e8f85b AS production

ENV FASTEMBED_CACHE_PATH=/home/nonroot/fastembed \
    PATH=/home/nonroot/.local/bin:$PATH

# skipcq: DOK-DL3018
RUN apk add --no-cache curl libstdc++

USER nonroot

WORKDIR /home/nonroot

COPY --from=builder --chown=nonroot:nonroot --chmod=555 /home/nonroot/.local/ /home/nonroot/.local/

EXPOSE 8081

CMD ["chatacter", "start"]
