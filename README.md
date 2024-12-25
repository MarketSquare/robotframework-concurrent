# robotframework-concurrent

## Purpose of this repo
This repo serves several tasks.
 - Show the current state of concurrent robotframework executions.
 - propose changes to robotframework
 - base the workshop at robocon about concurrency

## Ideas how to modify robotframework proper for better concurrency support

### process star
The currently presented solution uses subprocess.Popen, which is ok.
However _IF_ there would be code added to the startup code of the robotframework, we could use multiprocessing.Process, which on some platforms uses the Fork call which is way more efficient than Popen, and generally the better solution...

An anchor marker could be made available, to allow to be used as a reference point for suites.

### threads and async
Add a checker which warns/fails if a function or method is called from a thread which is not apropriate. This is going to bring runtime costs, and whil not work for functions/methods outside of our controll so it would propably be the most usefull if it is an optionally enabled feature.

## Advantages and disadvantages
| Tables        | process star           | async/thread  |
| ------------- |:-------------:| -----:|
| relation with other concurrancy solutions | everything goes | this solutin uses threads, dont mix with process based parallelism (Fork) |
| limitations on sharing data      | only pickleable, no references, no file objects      |   no limits |
| performance of data exchange | slower, large data needs to be copied      |    faster, references are possible |
| synchronisation bugs | not possible      |    avoidable, but possible |
| order in log is reliable | yes      |    no |

## Project todo list
improve quality controll (add mutation testing)
get real world usage examples out
