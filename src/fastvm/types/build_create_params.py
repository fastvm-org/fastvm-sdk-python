# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["BuildCreateParams"]


class BuildCreateParams(TypedDict, total=False):
    context_download_url: Annotated[str, PropertyInfo(alias="contextDownloadUrl")]
    """Presigned GET URL for a `tar.gz` of the build context.

    The worker downloads and extracts this into `/tmp/buildctx` before invoking
    buildah, so `COPY` instructions resolve against the user's files. Obtain via
    `POST /v1/build-contexts/presign`.
    """

    disk_gi_b: Annotated[int, PropertyInfo(alias="diskGiB")]
    """Disk size for the build VM. Defaults to 10 GiB if omitted."""

    dockerfile_content: Annotated[str, PropertyInfo(alias="dockerfileContent")]
    """Raw Dockerfile content to feed to `buildah bud` inside the build VM.

    Multi-stage, `SHELL`, `RUN --mount`, and every standard Dockerfile feature is
    supported (handled natively by buildah). Container-runtime metadata (`CMD`,
    `ENTRYPOINT`, `EXPOSE`, `LABEL`, `HEALTHCHECK`) is consumed by buildah but does
    not surface on the resulting FastVM snapshot — when the snapshot boots, systemd
    takes over, not the container's CMD.
    """

    image_ref: Annotated[str, PropertyInfo(alias="imageRef")]
    """Docker image reference (e.g.

    `python:3.13-slim`, `ghcr.io/user/repo:tag`). Used directly on the no-Dockerfile
    path, and as a fallback `FROM` source otherwise.
    """

    machine_type: Annotated[str, PropertyInfo(alias="machineType")]
    """Machine size identifier (e.g.

    `c1m2`, `c2m4`). Controls CPU and memory allocation. Must be supplied on launch
    unless restoring from a snapshot.
    """

    name: str
    """Optional human-readable name for the resulting snapshot.

    If omitted, the build ID is used.
    """
