One of the main challenges was finding a trade-off between ease of implementation and flexibility for future changes, such as modifying the board size, changing the machine-player algorithm, supporting two-player or even multiplayer/team-based games (including networked games using socket programming), adding a web-based backend, saving/retrieving game state, implementing a timer-based mode, adding a voice module, and so on.

The Strategy design pattern is used for both the *machinePlayer* and *gameWinner* algorithms because:

1. It allows the algorithm to be changed easily, even at runtime, through polymorphism.
2. Adding new algorithms in the future becomes simpler.
3. For games with large board sizes, the main performance bottlenecks are often the *machinePlayer* and/or *gameWinner* modules. To keep the game responsive, multithreading (thread pools) and/or asynchronous programming may be required for these components.

To achieve loose coupling, ease of unit testing and maintenance, and runtime polymorphism, abstract base (interface) classes are used together with dependency injection (DI). Because the game is not very complex at this stage, adding a full DI framework would slow down development and reduce readability (both for myself and for other developers). Therefore, I used the Factory Method to create objects for each class, and applied constructor-based DI to minimize the chance of bugs, while still allowing dependencies to be changed at runtime through getter/setter methods.

While singletons are generally not ideal for maintainability, they are used here only for a few parts such as default values that must remain constant during runtime (e.g., the 3×3 board size). This does not interfere with unit testing, because test modules can easily replace these values with simple integers without importing the singleton class.

The Observer design pattern is used to ensure loose coupling between components, so that adding future modules—such as networking, voice support, timers, etc.—will not require modifying existing classes.

Due to time limitations, unit and integration tests have not been fully implemented. A sample test is included for one module where bugs occurred during development.

