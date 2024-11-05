import java.util.*;

public class HashedHeap<T> {
    private List<T> heap; // This will store the heap elements
    private Map<T, Integer> indexMap; // This will map each value to its index in the heap
    private Comparator<T> comparator; // Comparator to decide the order of the heap

    public HashedHeap(Comparator<T> comparator) {
        this.heap = new ArrayList<>();
        this.indexMap = new HashMap<>();
        this.comparator = comparator;
    }

    public void add(T value) {
        if (indexMap.containsKey(value)) {
            return; // Optionally handle duplicate values or throw an exception
        }
        heap.add(value);
        int index = heap.size() - 1;
        indexMap.put(value, index);
        siftUp(index);
    }

    public T remove() {
        if (heap.isEmpty()) {
            return null;
        }
        return removeAt(0);
    }

    public T peek() {
        if (heap.isEmpty()) {
            return null;
        }
        return heap.get(0);
    }

    private T removeAt(int index) {
        if (index >= heap.size()) {
            return null;
        }

        T removedValue = heap.get(index);
        T lastValue = heap.remove(heap.size() - 1);
        indexMap.remove(removedValue);

        if (index < heap.size()) {
            heap.set(index, lastValue);
            indexMap.put(lastValue, index);
            // Decide to sift up or down based on the condition of the heap
            if (index > 0 && comparator.compare(heap.get(index), heap.get(parent(index))) < 0) {
                siftUp(index);
            } else {
                siftDown(index);
            }
        }
        return removedValue;
    }

    private void siftUp(int index) {
        T value = heap.get(index);
        while (index > 0) {
            int parentIndex = parent(index);
            T parentValue = heap.get(parentIndex);
            if (comparator.compare(value, parentValue) >= 0) {
                break;
            }
            heap.set(index, parentValue);
            indexMap.put(parentValue, index);
            index = parentIndex;
        }
        heap.set(index, value);
        indexMap.put(value, index);
    }

    private void siftDown(int index) {
        T value = heap.get(index);
        while (true) {
            int left = leftChild(index);
            int right = rightChild(index);
            int smallest = index;

            if (left < heap.size() && comparator.compare(heap.get(left), heap.get(smallest)) < 0) {
                smallest = left;
            }
            if (right < heap.size() && comparator.compare(heap.get(right), heap.get(smallest)) < 0) {
                smallest = right;
            }
            if (smallest == index) {
                break;
            }
            heap.set(index, heap.get(smallest));
            indexMap.put(heap.get(smallest), index);
            index = smallest;
        }
        heap.set(index, value);
        indexMap.put(value, index);
    }

    private int parent(int index) {
        return (index - 1) / 2;
    }

    private int leftChild(int index) {
        return 2 * index + 1;
    }

    private int rightChild(int index) {
        return 2 * index + 2;
    }

    public boolean isEmpty() {
        return heap.isEmpty();
    }

    public int size() {
        return heap.size();
    }

    public boolean contains(T value) {
        return indexMap.containsKey(value);
    }
}





public static void main(String[] args) {
    HashedHeap<Integer> maxHeap = new HashedHeap<>(Comparator.reverseOrder());
    HashedHeap<Integer> minHeap = new HashedHeap<>(Comparator.naturalOrder());

    maxHeap.add(5);
    maxHeap.add(2);
    maxHeap.add(10);
    System.out.println("Max Heap: " + maxHeap.remove()); // Should return 10

    minHeap.add(5);
    minHeap.add(2);
    minHeap.add(10);
    System.out.println("Min Heap: " + minHeap.remove()); // Should return 2
}
