from pawpal_system import Owner, Pet, Task, Scheduler

# --- Create Owner ---
owner = Owner("Shauna")

# --- Create Pets ---
dog = Pet(name="Biscuit", species="Dog", age=3)
cat = Pet(name="Luna", species="Cat", age=5)

owner.add_pet(dog)
owner.add_pet(cat)

# --- Create Tasks ---
walk = Task(title="Morning Walk", duration_minutes=30, priority="high", frequency="daily", pet=dog)
feed_dog = Task(title="Feed Biscuit", duration_minutes=10, priority="high", frequency="daily", pet=dog)
feed_cat = Task(title="Feed Luna", duration_minutes=10, priority="high", frequency="daily", pet=cat)
grooming = Task(title="Brush Luna", duration_minutes=15, priority="medium", frequency="weekly", pet=cat)
play = Task(title="Playtime", duration_minutes=20, priority="low", frequency="daily", pet=dog)

# --- Attach tasks to pets ---
dog.tasks.extend([walk, feed_dog, play])
cat.tasks.extend([feed_cat, grooming])

# --- Set up Scheduler ---
scheduler = Scheduler(owner=owner, available_minutes=60)

for task in owner.get_all_tasks():
    scheduler.add_task(task)

# --- Print Today's Schedule ---
print(f"\nOwner  : {owner}")
print(f"Pets   : {dog.get_info()}, {cat.get_info()}")
scheduler.explain_plan()
