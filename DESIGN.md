# Design notes

## Internal structure

`TriageQueue` keeps three deques, one for each triage level. `enqueue` appends the patient to the deque for that level. `dequeue` and `peek` look at level 1, then level 2, then level 3, and use the front of the first deque that has someone waiting.

A new level-1 patient is appended to the level-1 deque. That deque is already ahead of the level-2 and level-3 deques, so the new patient is ahead of every lower level without moving those patients and without sorting the whole queue.

A single deque would hold every level in one line. Putting a new level-1 patient in the right place would mean scanning that line or rebuilding it. A sorted list would re-sort, or shift elements to insert in the middle. A heap keeps priority order too, but each insertion and removal walks a tree. The three deques make adding a patient and calling the next patient direct front or back operations. Inside one level, the deque order is the arrival order.

## Two workers at the same moment

The removal of the patient being called has to finish before that patient is handed to the worker. `dequeue` does that with `popleft` on the chosen level's deque and returns the patient `popleft` removed. That patient is already out of the queue when the worker receives them.

The new critical patient's `enqueue` appends them to the level-1 deque. That append does not put back a patient who was already removed.

If a worker first read who was at the front and only later removed that patient, another worker could read the same patient, and both could be given that patient. Removing the patient first, and finishing that removal before the patient is returned, is the order that prevents the same patient from being processed twice.

If the new level-1 patient is appended before `dequeue` looks at level 1, that patient is who gets removed when nobody is already ahead of them in the level-1 deque. If `dequeue` has already removed the previous front patient, the new patient stays in level 1 and is not the patient who was just handed out.
