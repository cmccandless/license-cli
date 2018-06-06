# license-cli
CLI for [license-api
](https://github.com/cmccandless/license-api)

## Usage

```Bash
$ ./cli.py -h
usage: cli [-h] {status,list} ...

positional arguments:
  {status,list}

optional arguments:
  -h, --help     show this help message and exit
```

```Bash
$ ./cli.py list -h
usage: list [-h] [-r]
            [-p {commerical-use,modifications,distribution,private-use,patent-use} [{commerical-use,modifications,distribution,private-use,patent-use} ...]]
            [-c {include-copyright,document-change,network-use-disclose,same-license,same-license--file,same-license--library} [{include-copyright,document-change,network-use-disclose,same-license,same-license--file,same-license--library} ...]]
            [-l {trademark-use,liability,patent-use,warranty} [{trademark-use,liability,patent-use,warranty} ...]]

optional arguments:
  -h, --help            show this help message and exit
  -r, --rules
  -p {commerical-use,modifications,distribution,private-use,patent-use} [{commerical-use,modifications,distribution,private-use,patent-use} ...], --permissions {commerical-use,modifications,distribution,private-use,patent-use} [{commerical-use,modifications,distribution,private-use,patent-use} ...]
  -c {include-copyright,document-change,network-use-disclose,same-license,same-license--file,same-license--library} [{include-copyright,document-change,network-use-disclose,same-license,same-license--file,same-license--library} ...], --conditions {include-copyright,document-change,network-use-disclose,same-license,same-license--file,same-license--library} [{include-copyright,document-change,network-use-disclose,same-license,same-license--file,same-license--library} ...]
  -l {trademark-use,liability,patent-use,warranty} [{trademark-use,liability,patent-use,warranty} ...], --limitations {trademark-use,liability,patent-use,warranty} [{trademark-use,liability,patent-use,warranty} ...]
  ```

  ```Bash
  $ ./cli.py status -h
usage: status [-h]

optional arguments:
  -h, --help  show this help message and exit
  ```


## Bash completion

```Bash
source completion
```
