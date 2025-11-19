

The current code design is based on the assumption that the system running the game is powerful enough to execute the program on a single thread.
Consequently, multithreading and/or asynchronous programming is not required at this stage.
However, with future needs in mind (e.g., larger board sizes), the system is designed using object-oriented and modular principles so that architectural changes can be made more easily and the existing modules can be reused.

One of the main challenges was finding a trade-off between ease of implementation and flexibility for future changes—such as modifying the board size or shape, changing the machine-player (computer) algorithm, adding tournaments, supporting two-player or even multiplayer/team-based games (including networked games using socket programming), adding web-based APIs, saving and retrieving game state, implementing timer-based modes, adding a voice module, and so on.

The Strategy design pattern is used for both the *machinePlayer* and *gameWinner* algorithms because:

1. It allows algorithms to be changed easily, even at runtime, through polymorphism.
2. Adding new algorithms in the future becomes simpler.
3. For games with large board sizes, the main performance bottlenecks are often the *machinePlayer* and/or *gameWinner* modules. To keep the game responsive, multithreading (thread pools) and/or asynchronous programming may be required for these components. Using the Strategy pattern makes it easier to modify the architecture in the future and add multithreading.

To achieve loose coupling, ease of unit testing, maintainability, and runtime polymorphism, abstract base (interface) classes are used together with dependency injection (DI). Because the game is not very complex at this stage, adding a full DI framework would slow down development and reduce readability. Therefore, I used the Factory Method to create objects for each class and applied constructor-based DI to minimize the chance of bugs while still allowing dependencies to be changed at runtime through getter/setter methods.

While singletons are generally discouraged for maintainability, they are used here only for a few parts such as default values that must remain constant during runtime (e.g., the 3×3 board size). This does not interfere with unit testing because test modules can easily replace these values with simple integers without importing the singleton class.

The Observer design pattern is used to ensure loose coupling between components, allowing future modules—such as networking, voice support, timers, etc.—to be added without modifying existing classes. There are two observers: one for the GameEngine (*GEObserver*) and another for the application (*AppObserver*).

Since the GameEngine has only a limited number of states, using the State design pattern would increase boilerplate code unnecessarily. Therefore, simple switch/case or if/else logic is sufficient.

Due to time limitations, unit and integration tests have not yet been implemented.

Variable names, function names, and class names require further refinement to improve readability.
There are some inconsistencies between modules due to architectural changes made during development, and because of time constraints, these have not yet been fully resolved.


