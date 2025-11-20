
# Design Overview

The current code design is based on the assumption that the system running the game is powerful enough to execute the entire program on a single thread.
Consequently, multithreading and/or asynchronous programming is not required at this stage.

However, with future needs in mind (e.g., larger board sizes), the system is built using **object-oriented** and **modular** principles so that architectural changes can be made more easily and the existing modules can be reused.

---

## Design Challenges & Flexibility

One of the main challenges was finding a balance between **ease of implementation** and **flexibility for future expansion**, such as:

* Changing the board size or shape
* Modifying or replacing the machine-player (computer) algorithm
* Adding tournament or multi-round modes
* Supporting two-player or multiplayer/team-based games
* Enabling networked games (socket-based)
* Adding web-based APIs
* Saving/retrieving game state
* Implementing timer-based modes
* Adding a voice module
* And more…

---

## Use of the Strategy Pattern

The **Strategy design pattern** is used for both the `machinePlayer` and `gameWinner` algorithms because:

1. **Algorithms can be replaced easily**, even at runtime, through polymorphism.
2. **Adding new algorithms** in the future becomes simpler.
3. For large board sizes, these two modules usually become **performance bottlenecks**.

   * Future versions may require multithreading (thread pools) or asynchronous execution.
   * Using Strategy makes it easier to introduce such improvements without redesigning the system.

---

## Dependency Injection & Loose Coupling

To achieve **loose coupling**, **testability**, and **maintainability**, the project uses:

* **Abstract base classes (interfaces)**
* **Constructor-based dependency injection (DI)**
* **Factory Method** for object creation

A full DI framework is intentionally avoided at this stage because it would increase complexity and reduce readability, given the relatively small project size.

---

## Use of Singletons

While the Singleton pattern is generally discouraged, it is used here **only for a few constant runtime values**, such as:

* Default board size (e.g., 3×3)

This does not interfere with unit testing, because test modules can easily replace these values with plain integers without importing the singleton class.

---

## Observer Pattern for Notifications

The **Observer design pattern** is used to keep the components loosely coupled and future-proof.
This allows features such as networking, timers, logging, or voice modules to be added later **without modifying existing logic**.

There are **two observers**:

* `GEObserver` — for the GameEngine
* `AppObserver` — for the Application layer

Both observers receive events and can be extended independently.

---

## State Handling

The GameEngine has only a limited number of states.
Using the full **State design pattern** would add unnecessary boilerplate, so simple `if/else` or `match/case` logic is sufficient and clearer for the current scope.

---

## Testing & Naming Improvements

* Unit and integration tests have **not yet been implemented** due to time constraints.
* Some naming conventions and class/module structures still require refinement for improved readability.
* A few inconsistencies exist across modules because of architectural changes made during development, and these will be addressed in future revisions.

