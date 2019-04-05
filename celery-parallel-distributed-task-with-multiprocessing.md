##### https://stackoverflow.com/questions/23916413/celery-parallel-distributed-task-with-multiprocessing

Your goals are:

> Distribute your work to many machines (distributed computing/distributed parallel processing)
> Distribute the work on a given machine across all CPUs (multiprocessing/threading)

Celery can do both of these for you fairly easily. The first thing to understand is that each celery worker is configured by default to run as many tasks as there are CPU cores available on a system:

Concurrency is the number of prefork worker process used to process your tasks concurrently, when all of these are busy doing work new tasks will have to wait for one of the tasks to finish before it can be processed.

The default concurrency number is the number of CPU’s on that machine (including cores), you can specify a custom number using -c option. There is no recommended value, as the optimal number depends on a number of factors, but if your tasks are mostly I/O-bound then you can try to increase it, experimentation has shown that adding more than twice the number of CPU’s is rarely effective, and likely to degrade performance instead.

This means each individual task doesn't need to worry about using multiprocessing/threading to make use of multiple CPUs/cores. Instead, celery will run enough tasks concurrently to use each available CPU.

With that out of the way, the next step is to create a task that handles processing some subset of your list_of_millions_of_ids. You have a couple of options here - one is to have each task handle a single ID, so you run N tasks, where N == len(list_of_millions_of_ids). This will guarantee that work is evenly distributed amongst all your tasks, since there will never be a case where one worker finishes early and is just waiting around; if it needs work, it can pull an id off the queue. You can do this (as mentioned by John Doe) using the a celery group.

tasks.py:

        @app.task
        def process_id(item):
            id = item #long complicated equation here
            database.objects(newid=id).save()
            
And to execute the tasks:

        from celery import group
        from tasks import process_id

        jobs = group(process_id.s(item) for item in list_of_millions_of_ids)
        result = jobs.apply_async()
        
Another option is to break the list into smaller pieces, and distribute the pieces to your workers. This approach runs the risk of wasting some cycles, because you may end up with some workers waiting around while others are still doing work. However, the celery documentation notes that this concern is often unfounded:

Some may worry that chunking your tasks results in a degradation of parallelism, but this is rarely true for a busy cluster and in practice since you are avoiding the overhead of messaging it may considerably increase performance.

So, you may find that chunking the list and distributing the chunks to each task performs better, because of the reduced messaging overhead. You can probably also lighten the load on the database a bit this way, by calculating each id, storing it in a list, and then adding the whole list into the DB once you're done, rather than doing it one id at a time. The chunking approach would look something like this

tasks.py:

      @app.task
      def process_ids(items):
          for item in items:
              id = item #long complicated equation here
              database.objects(newid=id).save() # Still adding one id at a time, but you don't have to.
And to start the tasks:

        from tasks import process_ids

        jobs = process_ids.chunks(list_of_millions_of_ids, 30) # break the list into 30 chunks. Experiment with what number works best here.
        jobs.apply_async()
You can experiment a bit with what chunking size gives you the best result. You want to find a sweet spot where you're cutting down messaging overhead while also keeping the size small enough that you don't end up with workers finishing their chunk much faster than another worker, and then just waiting around with nothing to do.
