# IDIA Singularity Registry Server

The IDIA Singularity Registry Server (IDIA sregistry) is available for managing, organising, and sharing Singularity container images. Ilifu users are able to upload containers and manage who can use them. Public containers can be downloaded to any remote site using `SingularityCE` or `Apptainer`.

## Requirements

An ilifu user account is required to upload containers to the IDIA Singularity Registry repository, and to pull containers from private collections.
Pulling and pushing need SingularityCE `version 3.3.0+` (3.10 or newer is recommended) or Apptainer.

## Support

Contact ilifu support at support@ilifu.ac.za to get help with uploading or downloading containers from IDIA sregistry.

## Definitions

`Collection` describes a class of containers, or a project group for which containers are created. A collection can be public or private; a private collection is only visible to its owners and readers.<br />
`Container_name`, is the name of the container (this is usually the name of the primary software, the project group for which the container is created, or a custom name if the container includes multiple software packages without a clear primary packages).<br />
`Tag` is the version of the primary software package included in the container (example v6.5.0), a date to indicate different builds (2023-01-23), or another custom versioning method.<br />
`Team` is a group of users. Owners of a collection pick its owners and readers from the members of their teams.

## Available collections

To view available containers visit our web UI at https://sregistry.idia.ac.za/collections. All public container-collections are available without requiring an ilifu account. Each container's page also shows the commands to pull it.

## Adding the registry (once)

Add the registry as a remote endpoint and make it your default:

```bash
singularity remote add --no-login idia-registry https://sregistry.idia.ac.za
singularity remote use idia-registry
```

With Apptainer, use the same commands with `apptainer` in place of `singularity`. If you added the registry before, `remote add` reports that `idia-registry` already exists: just run `remote use`.

### Logging in

Public containers need no login. To pull from a private collection, or to push, log in with an access token:

```bash
singularity remote login idia-registry
```

To get a token, log in to the [webUI](https://sregistry.idia.ac.za), open the dropdown menu from your username at the top right and select Token (or go to https://sregistry.idia.ac.za/token). Copy the token (it will look something like: `742a2ca17065a2d0137f24ec30455a4a3cd3fe2e`) and paste it on the terminal. You should receive confirmation that the token is verified, as follows:

```console
Generate an access token at https://sregistry.idia.ac.za/auth/tokens, and paste it here.
Token entered will be hidden for security.
Access Token:
INFO:    Access Token Verified!
INFO:    Token stored in /users/walter/.singularity/remote.yaml
```

If you get an issue like:

```console
FATAL:   while verifying token: error response from server: Invalid Credentials
```

Get a new token from the token page and run `singularity remote login idia-registry` again. There is no need to add the remote again.

## Access/download available containers

Once the registry is added, pull a `container` in `collection` with `tag`:

```bash
singularity pull library://collection/container:tag
```

To pull a container called `wsclean` with a tag `v3.3` in a collection called `wsclean`, we use the cmd:

```bash
singularity pull library://wsclean/wsclean:v3.3
```

Containers in a private collection can only be pulled after [logging in](#logging-in) as one of the collection's owners or readers. Without a valid login, a private container is reported as not found.

**Note**: most public containers available in the IDIA sregistry are also available on ilifu at `/software/astro/containers/`. Please confirm whether the container already exists on the filesystem before pulling the container to ilifu storage.

Containers from the repository can be used within a job step, without creating the container image file, using the following examples:

Run the container:

```bash
singularity run library://collection/container:tag
```

Shell into the container:

```bash
singularity shell library://collection/container:tag
```

**Note**: containers used this way are stored in a local cache (usually `$HOME/.singularity/cache`, or `$HOME/.apptainer/cache` for Apptainer, if an alternative is not set using `SINGULARITY_CACHEDIR` or `APPTAINER_CACHEDIR`). The storage used for this can grow considerably over time and we recommend using `singularity cache clean -a` to remove images after use.

## Pushing containers to the registry

Any user with the IDIA/ilifu user account is able to push images to collections they own. First [add the registry](#adding-the-registry-once) and [log in](#logging-in).

### Collections

**NB**. You can only push containers to collections you are an owner of. Readers can view and pull a collection, but not push to it.

Pushing to a collection name that doesn't exist yet creates the collection, with you as its owner. You can also create it first: login via the [webUI](https://sregistry.idia.ac.za), go to [View Collection](https://sregistry.idia.ac.za/collections) and use the "New Collection" button. This is useful to make a collection private before its first push. Collection names are lowercase: other characters, such as `.` or `/`, are replaced by `-`.

### Push the container to your collection

You can check the remote status via `singularity remote status idia-registry`, and output would look like:

```console
INFO:    Checking status of remote: idia-registry
SERVICE    STATUS  VERSION  URI
Keyserver  OK      v1.0.0   https://sregistry.idia.ac.za
Library    OK      v1.0.0   https://sregistry.idia.ac.za
Token      OK      v1.0.0   https://sregistry.idia.ac.za
INFO:    Access Token Verified!

Valid authentication token set (logged in).
```

This means you are ready to push images.<br />
To push a container named `astror` to a collection `calibration`, run:

```bash
singularity push -U ASTRO-R.sif library://walter/calibration/astror:latest
```

In this command: `ASTRO-R.sif` is the local name of the container that I want to push, `walter` is my username, `calibration` is the name of the collection I am pushing the container to, `astror` is the name a container will have in the IDIA sregistry, `latest` is the tag of the container. `-U` pushes an unsigned container.

## Collection members and teams

Each collection has owners and readers:

- **Owners** can push containers to the collection, delete them, view private containers and change the collection's settings, including its owners and readers.
- **Readers** can view and pull containers in the collection, including private ones, but can't push.

An owner adds owners and readers on the collection's Settings page, under Members, picking users from the members of their teams.

A team is a group of users. The user who creates a team becomes its owner, and can add and remove members. A team doesn't give access to any collection by itself: it is how owners find the people to add to their collections.

Create a team:

- Go to webUI: https://sregistry.idia.ac.za/
- Click on the “Teams” tab in the navigation bar
- Choose a name, team name, and image.
- Decide if your team is “open” or “invite” only
- **invite** only means that an owner must send an invitation link.
- **open** means that anyone can join the team that is authenticated in the registry
