#include <tinycthread.h>
#include <stdio.h>
#include <math.h>


#define ARRAY_SIZE 1000000
#define NUM_THREADS 4

typedef struct {
    double* array;
    int start, end;
} ComputeRange;


int computeSquareRoots(void* arg) {
    ComputeRange* range = (ComputeRange*)arg;
    for (int i = range->start; i < range->end; i++) {
        range->array[i] = sqrt(range->array[i]);
    }

    return 0;
}


int main(void) {
    double results[ARRAY_SIZE];
    thrd_t threads[NUM_THREADS];
    ComputeRange ranges[NUM_THREADS];

    fprintf(stderr, "Starting computation with %d threads\n", NUM_THREADS);

    int chunk_size = ARRAY_SIZE / NUM_THREADS;
    for (int i = 0; i < NUM_THREADS; i++) {
        ranges[i].array = results;
        ranges[i].start = i * chunk_size;
        ranges[i].end = (i == NUM_THREADS - 1) ? ARRAY_SIZE : (i + 1) * chunk_size;
        if (thrd_create(&threads[i], computeSquareRoots, &ranges[i]) != thrd_success) {
            fprintf(stderr, "Failed to create thread %d\n", i);
        }
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        int ret = thrd_join(threads[i], NULL);
        if (ret != thrd_success) {
            fprintf(stderr, "Failed to join thread %d\n", i);
        }
    }

    printf("\nSample results:\n");
    for(int i = 0; i < 5; i++) {
        printf("sqrt(%d) = %f\n", i, results[i]);
    }

    printf("Computed %d square roots using %d threads\n", ARRAY_SIZE, NUM_THREADS);
    return 0;
}
