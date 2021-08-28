# Docker-Signatures

Docker signatures ensure that a Docker Image has all signatures.

# Why

This project helps you to parse "Docker trust inspect" command and checks if all the signatures you need are included in the Docker Image

# Install

```python
> pip install docker-signatures
```

# Usage examples

## Checking one signer

```console
> docker trust inspect --pretty dtr.example.com/admin/demo:1
Signatures for dtr.example.com/admin/demo:1

SIGNED TAG          DIGEST                                                             SIGNERS
1                   3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e   jeff

List of signers and their keys for dtr.example.com/admin/demo:1

SIGNER              KEYS
jeff                8ae710e3ba82

Administrative keys for dtr.example.com/admin/demo:1

  Repository Key:	10b5e94c916a0977471cc08fa56c1a5679819b2005ba6a257aa78ce76d3a1e27
  Root Key:	84ca6e4416416d78c4597e754f38517bea95ab427e5f95871f90d460573071fc
```

Checking if 'Paul' signature are included in Docker Image:

```console
> docker trust inspect --pretty dtr.example.com/admin/demo:1 | docker-signatures Paul 
[!] Missing signer: 'Paul'
> echo $?
1
```

Checking if 'jeff' signature are included in Docker Image: 

```console
> docker trust inspect --pretty dtr.example.com/admin/demo:1 | docker-signatures jeff
> echo $?
0 
```



## Checking any number of signers

```console
> docker trust inspect --pretty dtr.example.com/admin/demo:1
Signatures for dtr.example.com/admin/demo:1

SIGNED TAG          DIGEST                                                             SIGNERS
1                   3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e   jeff
2                   1111182b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e   Joan

List of signers and their keys for dtr.example.com/admin/demo:1

SIGNER              KEYS
jeff                8ae710e3ba82
Joan                8ae710e3bXXX

Administrative keys for dtr.example.com/admin/demo:1

  Repository Key:	10b5e94c916a0977471cc08fa56c1a5679819b2005ba6a257aa78ce76d3a1e27
  Root Key:	84ca6e4416416d78c4597e754f38517bea95ab427e5f95871f90d460573071fc
```

Checking that signatures of 'jeff' and 'Joan' are included: 

```console
> docker trust inspect --pretty dtr.example.com/admin/demo:1 | docker-signatures jeff Joan
> echo $?
0 
```

    NOTE: **docker-signatures** also works with JSON output of **docker trust inspect** command.


