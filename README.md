# MINESWEEPER-GAME-AI-PROJECT USING PROPOSITIONAL LOGIC
20PW31 AND 20PW39


Propositional logic is used in Minesweeper to infer which cells contain mines and which cells are safe to reveal. Each cell in the game board can be represented as a proposition, such as "A1 has a mine" or "B2 is safe to reveal". These propositions can be combined using logical operators to create complex statements that represent the game board.

For example, suppose that the game board is a 3x3 grid with the following information:

The cell at (1, 1) has one mine adjacent to it
The cell at (1, 2) has two mines adjacent to it
The cell at (2, 1) has no mines adjacent to it
The cell at (2, 2) has one mine adjacent to it
The cell at (2, 3) has one mine adjacent to it
The cell at (3, 2) has one mine adjacent to it
Using propositional logic, we can represent the state of the game board as a series of logical statements. For example, we can represent the fact that the cell at (1, 1) has one mine adjacent to it as the following statement:

(A1 ∧ ¬A2 ∧ ¬B1 ∧ ¬B2 ∧ ¬B3 ∧ ¬C1 ∧ ¬C2 ∧ ¬C3) → (¬A1 ∧ (B1 ∨ B2 ∨ C1 ∨ C2))

This statement says that if the cell at (1, 1) has one mine adjacent to it, then the cells around it must not have any mines. Furthermore, if the cell at (1, 1) does have a mine adjacent to it, then at least one of the cells around it must contain a mine.

By constructing a series of such logical statements, we can use propositional logic to infer which cells contain mines and which cells are safe to reveal. For example, if we know that the cell at (1, 1) has one mine adjacent to it, and we also know that the cell at (1, 2) has two mines adjacent to it, then we can infer that the cell at (2, 3) must contain a mine, since it is the only remaining cell adjacent to both (1, 1) and (1, 2).

By making such inferences and deductions using propositional logic, we can solve the Minesweeper game and reveal all the safe cells without detonating any mines.