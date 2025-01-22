# Understanding Priority, Fairshare and Quality of Service
The Slurm documentation [on priority](https://slurm.schedmd.com/priority_multifactor.html), [fairshare](https://slurm.schedmd.com/fair_tree.html) and [QOS](https://slurm.schedmd.com/qos.html) is very extensive; what follows here is a short summary of the principles behind priority and fairshare, and how to check what's going on with your jobs on ilifu.

## Multifactor Priority
Our Slurm is configured to use multifactor priority scheduling which uses a number of factors to determine a job's priority. For each job that's submitted to the cluster, these factors are used to calculate that job's priority. The weighting of these factors can change if they're found not to be giving a fair usage to all users of the cluster. At any time the weights of the factors can be checked as follows:
```shell
$ scontrol show config | grep PriorityWeight
PriorityWeightAge       = 500
PriorityWeightAssoc     = 0
PriorityWeightFairShare = 100000
PriorityWeightJobSize   = 12500
PriorityWeightPartition = 0
PriorityWeightQOS       = 20000
PriorityWeightTRES      = (null)
```
A description of each these factors can be found [here](https://slurm.schedmd.com/priority_multifactor.html#mfjppintro) however the most important factors are:
1. **JobSize**: This factor gives priority to jobs based on their size. In particular our cluster is configured to give priority to larger jobs; This can be checked by running `scontrol show config | grep PriorityFavorSmall`. A job that requests all the nodes in cluster will receive the maximum priority weighting here: `1.0 × 12500` while a single node job would receive a priority weighting of `0.02 × 12500` (assuming there were 50 nodes in the cluster).
2. **QOS**: The Quality of Service weighting is used to give interactive jobs a higher priority. Please note the [limits of the qos-interactive](tech_docs/running_jobs?id=interactive-slurm-sessions) QOS option.
3. **Age**: The age factor is intentionally set very small so that as jobs age their priority increases only slightly. This is so that the _FairShare_ factor is dominant in most cases.
4. **FairShare**: The fairshare factor is the primary means of making cluster usage fair amongst our users and is described in more detail below. The idea is that the ilifu cluster is funded in different proportions by various groups and they should be given proportional access to the cluster. Further, within the funding groups there are separate projects, and these projects can also be allocated proportional access through a hierarchical description. Finally, within each project the individual users can be found, where once again they can be assigned a different proportion of access.

If one needs to check the priority of your jobs you can see this, together with the individual factors, using the `sprio` command as follows:
<details>
<summary><code>sprio -u userA,userB,userC</code></summary>

```shell
sprio -u userA,userB,userC
          JOBID PARTITION     USER   PRIORITY       SITE        AGE  FAIRSHARE    JOBSIZE        QOS
        1019947 Main         userC      56778          0         83      56545        151          0
        1021758 Main         userA        502          0        143        209        151          0
        1021776 Main         userA        492          0        132        209        151          0
        1022250 Main         userC      56774          0         80      56545        151          0
        1022891 Main         userB        886          0        108        628        151          0
```

</details>

## Fairshare
Proportional access of the cluster is described using a hierarchy of shares given to funders, projects and users. Once the shares have been allocated, actual usage is taken into account. This considers all of an account's usage relative to other accounts and uses this to calculate a final FairShare value.

### Shares
As noted before the shares on the cluster are described in a hierarchical fashion, where at the top level there are funders, followed by projects and finally the users themselves.

The fairshare shares associated within the funder-level accounts is set to reflect the proportion of money invested in ilifu. In terms of ilifu's primary funders these values can be checked as follows:

<details>
<summary><code>sshare --format="Account,RawShares"</code></summary>

```shell
$ sshare --format="Account,RawShares" | grep " a\|Raw"
             Account  RawShares 
 a01-idia-ag                 33 
 a02-cbio-ag                 33 
 a03-dirisa-ag               42 
 a04-cchem-ag                 5
```
i.e. funding currently of ilifu is in the ratio IDIA:CBIO:DIRISA:CCHEM = 33:20:42:5.
</details>

The fairshare shares associated within projects are usually all the same, i.e. all the projects falling under a given funder have equal access to the cluster. This can be seen looking at say the first few idia projects as follows:

<details>
<summary><code>sshare --format="Account,RawShares" | head -n 30</code></summary>

```shell
$ sshare --format="Account,RawShares" | head -n 30
             Account  RawShares 
-------------------- ---------- 
root                            
 a01-idia-ag                 33 
  b01-ska-ag                  1 
  b02-mhongoose-ag            1 
  b03-idia-ag                 1 
   b03-idia-ag                1 
  b04-lensed-hi-ag            1 
  b05-pipelines-ag            1 
  b08-fornax-ag               1 
  b09-mightee-ag              1 
  b10-intensitymap-+          1 
  b11-vlbi-ag                 1 
  b15-pink-ag                 1 
  b17-mightee-ukzn-+          1 
  b19-meerlicht-ag            1 
  b20-mals-ag                 1 
  b21-ulx1-ag                 1 
  b23-smc-ag                  1 
  b24-thunderkat-ag           1 
  b26-laduma-ag               1 
  b27-m64-ngc151-ag           1 
  b28-hippo-ag                1 
  b32-mhishaps-ag             1 
  b34-admins-ag               1 
   b34-admins-ag              1 
  b36-vela-ag                 1 
  b37-rhodes-ratt-ag          1 
  b40-healy-a2626-ag          1
```

**Note**: One can see the hierarchical nature of the shares here.
</details>

CBIO has chosen however to give a higher priority to their primary project:

<details>
<summary><code>sshare --format="Account,RawShares | grep cbio</code></summary>

```shell
$ sshare --format="Account,RawShares" | grep cbio
 a02-cbio-ag                 20 
  b16-cbio-ag                 1 
   b16-cbio-ag                1 
  b56-cbio-001-ag            12 
  b57-cbio-002-ag             1 
  b58-cbio-003-ag             1 
  b67-cbio-004-ag             1 
  b70-cbio-005-ag             1 
  b83-cbio-006-ag             1 
  b85-cbio-007-ag             1 
  b88-cbio-008-ag             1 
  b89-cbio-009-ag             1 
  b90-cbio-010-ag             1 
  b93-cbio-011-ag             1 
  b99-cbio-012-ag             1
```

</details>

Finally all users within projects (on ilifu) have equal access within their projects.

<details>
<summary><code>sshare -a --format="Account,User,RawShares" | head -n 40</code></summary>

```shell
$ sshare -a --format="Account,User,RawShares" | head -n 40
             Account       User  RawShares 
-------------------- ---------- ---------- 
root                                       
 root                      root          1 
 a01-idia-ag                            33 
  b01-ska-ag                             1 
   b01-ska-ag             frank          1 
   b01-ska-ag              ianh          1 
   b01-ska-ag          isabella          1 
  b02-mhongoose-ag                       1 
   b02-mhongoose-ag    athomson          1 
   b02-mhongoose-ag        blok          1 
   b02-mhongoose-ag    djpisano          1 
   b02-mhongoose-ag       frank          1 
   b02-mhongoose-ag      gheald          1 
   b02-mhongoose-ag      grange          1 
   b02-mhongoose-ag  rontrompe+          1 
  b03-idia-ag                            1 
   b03-idia-ag         abonaldi          1 
   b03-idia-ag            adams          1 
   b03-idia-ag         adrianna          1 
   b03-idia-ag              afg          1 
   b03-idia-ag           aikema          1 
   b03-idia-ag          ajbaker          1 
   b03-idia-ag        ajvdhorst          1 
   b03-idia-ag          aleloni          1 
   b03-idia-ag       amirkazem+          1 
   b03-idia-ag        anastasia          1 
   b03-idia-ag             ando          1 
   b03-idia-ag             andy          1 
   b03-idia-ag            angus          1 
   b03-idia-ag             anke          1 
   b03-idia-ag          aparikh          1 
   b03-idia-ag          ascaife          1 
   b03-idia-ag       athanaseus          1 
   b03-idia-ag         athomson          1 
   b03-idia-ag            aycha          1 
   b03-idia-ag       bengelbre+          1 
   b03-idia-ag           bester          1 
   b03-idia-ag             blok          1
```

</details>

### Usage
Once the shares have been allocated the actual usage by users/accounts is considered. take for example two of the projects running on the cluster:

<details>
<summary><code>sshare -a --format="Account,User,RawUsage,FairShare,LevelFS"</code></summary>

```shell
$ sshare -a --format="Account,User,RawUsage,FairShare,LevelFS" | grep -v "inf" | grep "User\|b24\|b19"
             Account       User    RawUsage  FairShare    LevelFS 
  b19-meerlicht-ag                239670481              0.188518 
   b19-meerlicht-ag        andy         429   0.082723 1.5085e+04 
   b19-meerlicht-ag      nblago      350752   0.079581  18.467596 
   b19-meerlicht-ag         pmv   239299739   0.078534   0.027069 
   b19-meerlicht-ag    simdewet        2715   0.081675 2.3857e+03 
   b19-meerlicht-ag  sumedhabi+       16844   0.080628 384.545736 
  b24-thunderkat-ag               493709909              0.091516 
   b24-thunderkat-ag     bright    10095018   0.007330   1.086806 
   b24-thunderkat-ag      dante        4697   0.017801 2.3358e+03 
   b24-thunderkat-ag francesco+        3061   0.019895 3.5840e+03 
   b24-thunderkat-ag       ianh    42273760   0.003141   0.259531 
   b24-thunderkat-ag jakobvand+     2392664   0.011518   4.585403 
   b24-thunderkat-ag   jcollier        4272   0.018848 2.5677e+03 
   b24-thunderkat-ag    jgirard        1401   0.023037 7.8256e+03 
   b24-thunderkat-ag   jkersten     4417718   0.009424   2.483483 
   b24-thunderkat-ag    jmoldon        5039   0.016754 2.1769e+03 
   b24-thunderkat-ag   julioanj    16789261   0.005236   0.653473 
   b24-thunderkat-ag kelebogil+        2339   0.020942 4.6886e+03 
   b24-thunderkat-ag laurenrho+     3995881   0.010471   2.745660 
   b24-thunderkat-ag  madzimest        5670   0.015707 1.9347e+03 
   b24-thunderkat-ag    mcoriat           0   0.025131 1.9313e+08 
   b24-thunderkat-ag reikantse+      248307   0.013613  44.184462 
   b24-thunderkat-ag      retha        1884   0.021990 5.8216e+03 
   b24-thunderkat-ag     robbie     1290421   0.012565   8.502129 
   b24-thunderkat-ag sarahchas+   284738897   0.001047   0.038531 
   b24-thunderkat-ag        sem    86446084   0.002094   0.126915 
   b24-thunderkat-ag     tremou     6597117   0.008377   1.663049 
   b24-thunderkat-ag     wenfei         363   0.024084 3.0165e+04 
   b24-thunderkat-ag  williamsd    19899115   0.004188   0.551348 
   b24-thunderkat-ag       xian      227163   0.014660  48.297169 
   b24-thunderkat-ag      zwang    14269763   0.006283   0.768852
```

Here we see that the one project has approximately twice the usage of the other project, resulting in the users within the projects having dramatically different FairShare values.

</details>

A note on **LevelFS**: This gives an indication whether an account is using more or less than is allocated to it via the shares. A value of 1 indicates a perfect usage, less than 1 indicates more usage than allocated and more than 1 means it is underused. It is very unlikely that these values will be exactly 1, however over a long period of time, assuming all users/groups are active, they should tend towards 1.

<details>
<summary><code>sshare --format="Account,RawShares,RawUsage,LevelFS" | grep -v "inf" | grep "Shares\|a0</code></summary>

```shell
$ sshare --format="Account,RawShares,RawUsage,LevelFS" | grep -v "inf" | grep "Shares\|a0"
             Account  RawShares    RawUsage    LevelFS 
 a01-idia-ag                 33  2078039237   0.423716 
 a02-cbio-ag                 20   578477684   0.922482 
 a03-dirisa-ag               42    37792325  29.652425 
 a04-cchem-ag                 5       27631 4.8281e+03
```

</details>

And lastly we consider [PriorityDecayHalfLife](https://slurm.schedmd.com/priority_multifactor.html#config). This indicates how long past usage counts towards the fairshare calculation. On ilifu this is currently set to a half life of 14 days, i.e. every 14 days the accumulated usage is halved. This value can be checked in the configuration using:

<details>
<summary><code>scontrol show config | grep Decay</code></summary>

```shell
$ scontrol show config | grep Decay
PriorityDecayHalfLife   = 14-00:00:00
```
This is calculated every 5 minutes.
```shell
$ scontrol show config | grep PriorityCalcPeriod
PriorityCalcPeriod      = 00:05:00
```

</details>

## Quality of Service (QOS)

The QOS settings on ilifu are another limit put in place that is used to limit the amount of resources research projects or users have access to. This is used to ensure that the cluster is not overused by a single user or project. The QOS settings can be checked using the `sacctmgr` command as follows:


```shell
$ sacctmgr show qos format="Name%20,GrpTRESRunMins%32,MaxTRESPA%32,MaxTRESPU%35,MaxJobsPU"
                Name                   GrpTRESRunMins                        MaxTRESPA                           MaxTRESPU MaxJobsPU
-------------------- -------------------------------- -------------------------------- ----------------------------------- ---------
              normal                                               cpu=2105,mem=15265G                  cpu=1203,mem=8723G     10000
     qos-interactive                                                                                  cpu=4,mem=28G,node=1         1
             jupyter      cpu=99999999,mem=530491648G      cpu=99999999,mem=530491648G
               devel      cpu=99999999,mem=530491648G      cpu=99999999,mem=530491648G
        a01-idia-qos      cpu=17998848,mem=130491648G              cpu=2105,mem=15265G                  cpu=1203,mem=8723G     10000
        a02-cbio-qos      cpu=17998848,mem=130491648G              cpu=2105,mem=15265G                  cpu=1203,mem=8723G     10000
      a03-dirisa-qos      cpu=17998848,mem=130491648G              cpu=2105,mem=15265G                  cpu=1203,mem=8723G     10000
       a04-cchem-qos      cpu=17998848,mem=130491648G              cpu=2105,mem=15265G                  cpu=1203,mem=8723G     10000
         highmem_qos
             gpu-qos                                                 cpu=192,mem=1440G         cpu=128,gres/gpu=4,mem=960G
```

The `GrpTRESRunMins` (or Group Trackable Resource Running Minutes) is used to control the amount of resources a project/account has access to over time. These are
calculated as a percentage of the cluster over time, e.g. for IDIA projects the limit is currently set to `cpu=17998848,mem=130491648G` which means that approximately
65% of the cluster can be used for 7 days continuously. i.e. if the total remaining resources allocated to running IDIA jobs nears this limit, the scheduler will not
start new IDIA jobs.

The `MaxTRESPA` limits the instantaneous amount of resources allocated to an account. In the case of IDIA projects this is set to `cpu=2105,mem=15265G` which means that
at most 70% of the cluster can be used by IDIA jobs at any one time.

The `MaxTRESPU` setting the instantaneous amount of resources allocated to a specific user. A setting of `cpu=1203,mem=8723G` means that at most 40% of the cluster can be
allocated to a single user at any one time.

Finally the `MaxJobsPU` setting limits the number of jobs a user can run at any one time.
