#include <stdio.h>
#include <stdlib.h>

#define ROWS 5
#define COLS 5

// Structure for a grid cell
typedef struct {
    int x, y;
} Cell;

// Possible movements in 4 directions (up, down, left, right)
int rowMoves[] = {-1, 1, 0, 0};
int colMoves[] = {0, 0, -1, 1};

// Function to perform BFS in a grid
void bfs(int grid[ROWS][COLS], int startX, int startY) {
    int visited[ROWS][COLS] = {0};
    Cell queue[ROWS * COLS];
    int front = 0, rear = 0;

    // Starting point
    queue[rear++] = (Cell){startX, startY};
    visited[startX][startY] = 1;

    printf("BFS Traversal starting from (%d, %d):\n", startX, startY);

    while (front < rear) {
        Cell current = queue[front++];
        printf("(%d, %d) -> ", current.x, current.y);

        // Explore neighbors
        for (int i = 0; i < 4; i++) {
            int newRow = current.x + rowMoves[i];
            int newCol = current.y + colMoves[i];

            if (newRow >= 0 && newRow < ROWS && newCol >= 0 && newCol < COLS &&
                grid[newRow][newCol] == 1 && !visited[newRow][newCol]) {
                visited[newRow][newCol] = 1;
                queue[rear++] = (Cell){newRow, newCol};
            }
        }
    }
    printf("End of BFS\n");
}

int main() {
    int grid[ROWS][COLS] = {
        {1, 0, 1, 1, 1},
        {1, 1, 0, 0, 1},
        {0, 1, 1, 0, 1},
        {1, 0, 1, 1, 1},
        {1, 1, 0, 1, 1}
    };

    // Start BFS from top-left corner (0, 0)
    bfs(grid, 0, 0);
    return 0;
}
