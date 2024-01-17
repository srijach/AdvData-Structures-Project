import sys

class MinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.curr_size = 0

    def insert(self, ele):
        # Append the new element to the end of the heap list
        self.heap_list.append(ele)

        # Increase the size of the heap by 1
        self.curr_size += 1

        # Move the new element up the heap until it is in the correct position
        self.bubble_up(self.curr_size)

    def swap(self, ind1, ind2):
        # Store the element at ind1 in a temporary variable
        temp = self.heap_list[ind1]

        # Swap the elements at ind1 and ind2
        self.heap_list[ind1] = self.heap_list[ind2]
        self.heap_list[ind2] = temp

        # Update the indices of the swapped elements in the heap_list
        # so that they can be located and swapped again if necessary
        self.heap_list[ind1].min_heap_index = ind1
        self.heap_list[ind2].min_heap_index = ind2

    def get_minchild(self, p):
        # Check if the left child index is out of range for the heap list
        if (p * 2) + 1 > self.curr_size:
            # Return the index of the right child (which doesn't exist)
            return p * 2
        else:
            # Compare the left and right child elements and return the index
            # of the minimum one
            if self.heap_list[p * 2].ride.less_than(self.heap_list[(p * 2) + 1].ride):
                return p * 2
            else:
                return (p * 2) + 1

    def update_element(self, p, new_key):
        # Get the node at index p
        node = self.heap_list[p]

        # Update the key of the ride associated with the node
        node.ride.triptime = new_key

        # If the node is the root of the heap, bubble down
        if p == 1:
            self.bubble_down(p)
        # If the node's parent has a smaller ride, bubble down
        elif self.heap_list[p // 2].ride.less_than(self.heap_list[p].ride):
            self.bubble_down(p)
        # Otherwise, bubble up
        else:
            self.bubble_up(p)

    def delete_element(self, p):
        # Swap the element to be deleted with the last element in the heap
        self.swap(p, self.curr_size)

        # Decrement the size of the heap
        self.curr_size -= 1

        # Delete the last element from the heap list using tuple unpacking
        *self.heap_list, _ = self.heap_list

        # Move the swapped element down the heap until it is in the correct position
        self.bubble_down(p)

    def bubble_up(self, p):
        # While the parent of the current node is valid (i.e., not the root)
        while (p // 2) > 0:
            # If the current node is less than its parent, swap them
            if self.heap_list[p].ride.less_than(self.heap_list[p // 2].ride):
                self.swap(p, (p // 2))
            # Otherwise, break out of the loop
            else:
                break
            # Move up to the parent node
            p = p // 2

    def bubble_down(self, p):
        # While the left child of the current node is valid (i.e., not out of range)
        while (p * 2) <= self.curr_size:
            # Get the index of the child with the minimum ride
            ind = self.get_minchild(p)

            # If the current node is greater than its minimum child, swap them
            if not self.heap_list[p].ride.less_than(self.heap_list[ind].ride):
                self.swap(p, ind)

            # Move down to the minimum child node
            p = ind

    def pop(self):
        # Check if there are any rides available in the heap
        if len(self.heap_list) == 1:
            return 'No Rides Available'

        # Get the root node (i.e., the ride with the minimum trip duration)
        root = self.heap_list[1]

        # Swap the root node with the last element in the heap
        self.swap(1, self.curr_size)
        self.curr_size -= 1

        # Delete the last element from the heap list using tuple unpacking
        *self.heap_list, _ = self.heap_list

        # Move the swapped element down the heap until it is in the correct position
        self.bubble_down(1)

        # Return the root node (i.e., the ride with the minimum trip duration)
        return root


class MinHeapNode:
    def __init__(self, ride, rbt_node, min_heap_index):
        """
        Initialize a MinHeapNode object.

        Parameters:
        ride (Ride): The Ride object associated with this MinHeapNode.
        rbt_node (RBTNode): The RBTNode object associated with this MinHeapNode.
        min_heap_index (int): The index of this MinHeapNode in the min heap.
        """
        self.ride = ride
        self.rbt_node = rbt_node
        self.min_heap_index = min_heap_index



class RBTNode:
    def __init__(self, ride, min_heap_node):
        """
        Create a new RBTNode object.

        Arguments:
        - ride: a Ride object to be stored in this node
        - min_heap_node: the MinHeapNode object associated with the ride
        """
        self.ride = ride
        self.pp = None  # initialize pp node to None
        self.left = None  # initialize left node to None
        self.right = None  # initialize right node to None
        self.color = 1  # initialize color to red (1) by default
        self.min_heap_node = min_heap_node



class RedBlackTree:
    def __init__(self):
        self.null_node = RBTNode(None, None)
        self.null_node.left = None
        self.null_node.right = None
        self.null_node.color = 0
        self.root = self.null_node

    # To retrieve the ride with the ride_num equal to the key
    def get_ride(self, key):
        temp = self.root

        # Iterating through the tree to find the node with ride_num equal to the key
        while temp != self.null_node:
            if temp.ride.ride_num == key:
                return temp
            elif temp.ride.ride_num < key:
                temp = temp.right
            else:
                temp = temp.left

        # If the ride with the specified ride_num was not found, return None
        return None

    def findrange(self, node, low, high, res):
        if node == self.null_node:
            return

        # Traverse left subtree if the current node's ride_num is greater than low
        if low < node.ride.ride_num:
            self.findrange(node.left, low, high, res)

        # Add the current ride to result list if it falls within the range [low, high]
        if low <= node.ride.ride_num <= high:
            res.append(node.ride)

        # Traverse right subtree if the current node's ride_num is less than high
        self.findrange(node.right, low, high, res)

    def getrange(self, low, high):
        res = []
        # Call the helper function to find rides falling within the range [low, high]
        self.findrange(self.root, low, high, res)
        # Return the list of rides falling within the range
        return res

    def repnode(self, node, c_node):
        # If the node to be replaced is the root node
        if node.pp is None:
            self.root = c_node
        # If the node to be replaced is a right child of its parent
        elif node == node.pp.right:
            node.pp.right = c_node
        # If the node to be replaced is a left child of its parent
        else:
            node.pp.left = c_node
        # Update the parent pointer of the child node to be the same as the parent of the original node
        c_node.pp = node.pp

    def deletenodehelp(self, node, key):
        # Search for the node to delete
        deleten = self.null_node
        while node != self.null_node:
            if node.ride.ride_num == key:
                deleten = node
            if node.ride.ride_num >= key:
                node = node.left
            else:
                node = node.right

        # If the node to delete is not found, return
        if deleten == self.null_node:
            return

        # Get the min heap node associated with the node to delete
        heap_node = deleten.min_heap_node

        # Get the node to be spliced out of the tree
        y = deleten
        y_original_color = y.color

        # Determine which node to splice in
        if deleten.left == self.null_node:
            x = deleten.right
            self.repnode(deleten, deleten.right)
        elif (deleten.right == self.null_node):
            x = deleten.left
            self.repnode(deleten, deleten.left)
        else:
            # If the node has two children, find its successor (minimum node in the right subtree)
            y = self.minimum(deleten.right)
            y_original_color = y.color
            x = y.right
            if y.pp == deleten:
                x.pp = y
            else:
                self.repnode(y, y.right)
                y.right = deleten.right
                y.right.pp = y

            # Replace the node to delete with its successor
            self.repnode(deleten, y)
            y.left = deleten.left
            y.left.pp = y
            y.color = deleten.color

        # If the color of the node spliced out was black, fix the tree to maintain red-black properties
        if y_original_color == 0:
            self.post_delete_fix(x)

        return heap_node

    # Balancing the tree after deletion
    def post_delete_fix(self, node):
        # Iterate until the node is the root or a red node
        while node != self.root and node.color == 0:
            # If the node is the right child
            if node == node.pp.right:
                # Get the sibling of the parent node
                parent_sibling = node.pp.left
                # If the sibling is red
                if parent_sibling.color != 0:
                    # Recolor the parent and sibling
                    node.pp.color = 1
                    parent_sibling.color = 0
                    # Perform a right rotation on the parent
                    self.rightro(node.pp)
                    # Update the sibling to the left child of the new parent
                    parent_sibling = node.pp.left

                # If both children of the sibling are black
                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    # Recolor the sibling and set the current node to its parent
                    parent_sibling.color = 1
                    node = node.pp
                else:
                    # If the left child of the sibling is not red
                    if parent_sibling.left.color != 1:
                        # Recolor the sibling and its right child
                        parent_sibling.right.color = 0
                        parent_sibling.color = 1
                        # Perform a left rotation on the sibling
                        self.leftro(parent_sibling)
                        # Update the sibling to the left child of the new parent
                        parent_sibling = node.pp.left

                    # Recolor the sibling and parent, and its left child
                    parent_sibling.color = node.pp.color
                    node.pp.color = 0
                    parent_sibling.left.color = 0
                    # Perform a right rotation on the parent
                    self.rightro(node.pp)
                    # Set the node to the root
                    node = self.root
            # If the node is the left child
            else:
                # Get the sibling of the parent node
                parent_sibling = node.pp.right
                # If the sibling is red
                if parent_sibling.color != 0:
                    # Recolor the parent and sibling
                    node.pp.color = 1
                    parent_sibling.color = 0
                    # Perform a left rotation on the parent
                    self.leftro(node.pp)
                    # Update the sibling to the right child of the new parent
                    parent_sibling = node.pp.right

                # If both children of the sibling are black
                if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                    # Recolor the sibling and set the current node to its parent
                    parent_sibling.color = 1
                    node = node.pp
                else:
                    # If the right child of the sibling is not red
                    if parent_sibling.right.color != 1:
                        # Recolor the sibling and its left child
                        parent_sibling.left.color = 0
                        parent_sibling.color = 1
                        # Perform a right rotation on the sibling
                        self.rightro(parent_sibling)
                        # Update the sibling to the right child of the new parent
                        parent_sibling = node.pp.right

                    # Recolor the sibling and parent, and its right child
                    parent_sibling.color = node.pp.color
                    node.pp.color = 0
                    parent_sibling.right.color = 0
                    # Perform a left rotation on the parent
                    self.leftro(node.pp)
                    # Set the node to the root
                    node = self.root

        # Recolor the node to black
        node.color = 0

    def post_insert_fix(self, curr_node):
        # Loop until the parent of the current node is not red
        while curr_node.pp.color == 1:
            if curr_node.pp == curr_node.pp.pp.left:
                # Case 1: The parent of the current node is a left child
                parent_sibling = curr_node.pp.pp.right

                if parent_sibling.color == 0:
                    # Case 1.1: The parent's sibling is black
                    if curr_node == curr_node.pp.right:
                        # Case 1.1.1: The current node is a right child
                        curr_node = curr_node.pp
                        self.leftro(curr_node)
                    curr_node.pp.color = 0
                    curr_node.pp.pp.color = 1
                    self.rightro(curr_node.pp.pp)
                else:
                    # Case 1.2: The parent's sibling is red
                    parent_sibling.color = 0
                    curr_node.pp.color = 0
                    curr_node.pp.pp.color = 1
                    curr_node = curr_node.pp.pp

            else:
                # Case 2: The parent of the current node is a right child
                parent_sibling = curr_node.pp.pp.left
                if parent_sibling.color == 0:
                    # Case 2.1: The parent's sibling is black
                    if curr_node == curr_node.pp.left:
                        # Case 2.1.1: The current node is a left child
                        curr_node = curr_node.pp
                        self.rightro(curr_node)
                    curr_node.pp.color = 0
                    curr_node.pp.pp.color = 1
                    self.leftro(curr_node.pp.pp)
                else:
                    # Case 2.2: The parent's sibling is red
                    parent_sibling.color = 0
                    curr_node.pp.color = 0
                    curr_node.pp.pp.color = 1
                    curr_node = curr_node.pp.pp

            if curr_node == self.root:
                break
        # Set the root color to black
        self.root.color = 0

    def minimum(self, node):
        # Loop through the left subtree of the node until you reach the leftmost node
        while node.left != self.null_node:
            node = node.left
        return node

    def leftro(self, x):
        # Save the right child of x as y
        y = x.right

        # Set the left child of y as the right child of x
        x.right = y.left
        if y.left != self.null_node:
            y.left.pp = x

        # Set the parent of y as the parent of x
        y.pp = x.pp
        if x.pp == None:
            # If x is the root, set y as the new root
            self.root = y
        elif x == x.pp.left:
            # If x is the left child of its parent, set y as the new left child of the parent
            x.pp.left = y
        else:
            # If x is the right child of its parent, set y as the new right child of the parent
            x.pp.right = y

        # Set the left child of x as y, and set the parent of y as x
        y.left = x
        x.pp = y

    def rightro(self, x):
        # Store the left child of x in y
        y = x.left

        # Set the right child of y to the left child of x
        x.left = y.right

        # If y's right child is not the null node, set its parent to x
        if y.right != self.null_node:
            y.right.pp = x

        # Set the parent of y to the parent of x
        y.pp = x.pp

        # Update the parent of x's child to y
        if x.pp == None:
            self.root = y
        elif x == x.pp.right:
            x.pp.right = y
        else:
            x.pp.left = y

        # Set the right child of y to x, and set the parent of x to y
        y.right = x
        x.pp = y

    def insert(self, ride, min_heap):
        # Create a new node with the given ride and min_heap
        node = RBTNode(ride, min_heap)

        # Set the node's parent, left child, right child, and color
        node.pp = None
        node.left = self.null_node
        node.right = self.null_node
        node.color = 1

        # Traverse the tree to find the correct position to insert the node
        insertion_node = None
        temp_node = self.root

        while temp_node != self.null_node:
            insertion_node = temp_node
            if node.ride.ride_num < temp_node.ride.ride_num:
                temp_node = temp_node.left
            else:
                temp_node = temp_node.right

        # Set the node's parent to the insertion_node, and update the insertion_node's children
        node.pp = insertion_node
        if insertion_node is None:
            self.root = node
        elif node.ride.ride_num > insertion_node.ride.ride_num:
            insertion_node.right = node
        else:
            insertion_node.left = node

        # If the node's parent is the root, color the node black and return
        if node.pp is None:
            node.color = 0
            return

        # If the node's grandparent is None, return
        if node.pp.pp is None:
            return

        # Fix the tree to maintain the properties of a red-black tree after insertion
        self.post_insert_fix(node)

    def deleten(self, ride_num):
        # Call the recursive helper method to delete the node with the given ride_num
        return self.deletenodehelp(self.root, ride_num)


class Ride:
    def __init__(self, ride_num, cost_ride, triptime):
        # Initialize a new Ride object with the given ride number, cost, and trip duration.
        self.ride_num = ride_num
        self.cost_ride = cost_ride
        self.triptime = triptime

    def less_than(self, other_ride):
        """Compare two Ride objects based on their cost and trip duration.

        Returns True if self is less expensive than other_ride, or if they have the same cost but self has a shorter trip
        duration. Returns False otherwise.
        """
        if self.cost_ride < other_ride.cost_ride:
            # If self's cost is less than other_ride's cost, return True (self is less than other_ride).
            return True
        elif self.cost_ride > other_ride.cost_ride:
            # If self's cost is greater than other_ride's cost, return False (self is not less than other_ride).
            return False
        elif self.cost_ride == other_ride.cost_ride:
            # If self's cost is equal to other_ride's cost, compare their trip durations.
            if self.triptime > other_ride.triptime:
                # If self's trip duration is greater than other_ride's trip duration, return False (self is not less than other_ride).
                return False
            else:
                # If self's trip duration is less than or equal to other_ride's trip duration, return True (self is less than other_ride).
                return True



def insert_ride(ride, heap, rbt):
    # Check if the ride_num already exists in the Red-Black Tree
    if rbt.get_ride(ride.ride_num) is not None:
        write_to_output(None, "Duplicate ride_num", False)
        sys.exit(0)
        return

    # Create a new RBTNode and MinHeapNode for the ride
    rbt_node = RBTNode(None, None)
    min_heap_node = MinHeapNode(ride, rbt_node, heap.curr_size + 1)

    # Insert the MinHeapNode into the Min Heap and the ride into the Red-Black Tree
    heap.insert(min_heap_node)
    rbt.insert(ride, min_heap_node)


def print_ride(ride_num, rbt):
    # Get the ride corresponding to the ride number from the Red-Black Tree
    res = rbt.get_ride(ride_num)

    # If the ride does not exist, add a dummy ride to the output with a message
    if res is None:
        write_to_output(Ride(0, 0, 0), "Ride not found", False)
    # If the ride exists, add it to the output without a message
    else:
        write_to_output(res.ride, "", False)


def print_rides(lower_bound, upper_bound, rbt):
    """
    Prints all rides whose ride numbers are within the specified range [lower_bound, upper_bound],
    using the provided Red-Black Tree object. The rides are printed to the output file in ascending order
    of ride numbers.
    """
    rides = rbt.getrange(lower_bound, upper_bound)
    write_to_output(rides, "", True)



def get_next_ride(heap, rbt):
    # If the Min Heap is not empty, pop the top element from the heap
    if heap.curr_size != 0:
        popped_node = heap.pop()
        # Delete the corresponding node from the Red-Black Tree
        rbt.deleten(popped_node.ride.ride_num)
        # Output the popped ride to the user
        write_to_output(popped_node.ride, "", False)
    else:
        # If the Min Heap is empty, output "No active ride requests" to the user
        write_to_output(None, "No active ride requests", False)



def cancel_ride(ride_number, heap, rbt):
    # Delete the ride from the Red-Black Tree and obtain the corresponding heap node
    heap_node = rbt.deleten(ride_number)

    # If the heap node exists, delete the corresponding element from the Min Heap
    if heap_node is not None:
        heap.delete_element(heap_node.min_heap_index)


def update_ride(ride_num, new_duration, heap, rbt):
    # Get the ride from the Red-Black Tree
    rbt_node = rbt.get_ride(ride_num)

    # If the ride does not exist, print message
    if rbt_node is None:
        print("")
    else:
        # If new duration is less than or equal to current duration, just update the heap
        if new_duration <= rbt_node.ride.triptime:
            heap.update_element(rbt_node.min_heap_node.min_heap_index, new_duration)
        # If the new duration is between current duration and twice the current duration, cancel the ride and insert a new ride with updated duration and cost
        elif rbt_node.ride.triptime < new_duration <= (2 * rbt_node.ride.triptime):
            cancel_ride(rbt_node.ride.ride_num, heap, rbt)
            insert_ride(Ride(rbt_node.ride.ride_num, rbt_node.ride.cost_ride + 10, new_duration), heap, rbt)
        # If the new duration is more than twice the current duration, cancel the ride
        else:
            cancel_ride(rbt_node.ride.ride_num, heap, rbt)

def write_to_output(ride, message, is_list):
    # Open the output file in append mode
    with open("output_file.txt", "a") as file:
        # If the ride is None, write the message to the output file
        if ride is None:
            file.write(message + "\n")
        else:
            # If the ride is not None, write the ride information to the output file
            if not is_list:
                # If the ride is not a list, write the ride information as a string
                message = f"({ride.ride_num},{ride.cost_ride},{ride.triptime})\n"
            else:
                # If the ride is a list, convert the list of rides to a string
                if len(ride) == 0:
                    message = "(0,0,0)\n"
                else:
                    rides_str = ",".join(f"({r.ride_num},{r.cost_ride},{r.triptime})" for r in ride)
                    message = f"{rides_str}\n"
            # Write the message to the output file
            file.write(message)
            
            

def main():

    if len(sys.argv) < 2:
        print("Invalid Arguments")
        print("Enter Command of the form : python3 gator_taxi.py <input_file_name.txt>")
        return


    ride_heap = MinHeap()
    ride_tree = RedBlackTree()

    # Open input and output files
    with open(sys.argv[1], "r") as input_file, open("output_file.txt", "w") as output_file:
        # Iterate over each line in the input file
        for line in input_file.readlines():
            # Parse the ride details from the line
            ride_details = []
            ride_details = [int(num) for num in line[line.index("(") + 1:line.index(")")].split(",") if num != '']

            # Determine the operation based on the line content and execute it
            if "Insert" in line:
                # Create a new ride object and insert it into the ride heap and tree
                new_ride = Ride(ride_details[0], ride_details[1], ride_details[2])
                insert_ride(new_ride, ride_heap, ride_tree)
            elif "UpdateTrip" in line:
                # Update the trip duration of an existing ride in the ride heap and tree
                ride_index = ride_details[0]
                new_duration = ride_details[1]
                update_ride(ride_index, new_duration, ride_heap, ride_tree)
            elif "GetNextRide" in line:
                # Get the ride with the earliest start time from the ride heap and remove it from both the heap and tree
                get_next_ride(ride_heap, ride_tree)
            elif "CancelRide" in line:
                # Cancel an existing ride by removing it from both the heap and tree
                ride_index = ride_details[0]
                cancel_ride(ride_index, ride_heap, ride_tree)
            elif "Print" in line:
                # Print either a single ride or a range of rides from the ride tree
                if len(ride_details) == 1:
                    ride_index = ride_details[0]
                    print_ride(ride_index, ride_tree)
                elif len(ride_details) == 2:
                    start_index = ride_details[0]
                    end_index = ride_details[1]
                    print_rides(start_index, end_index, ride_tree)

    # Close the output file
    output_file.close()


if __name__ == "__main__":
    main()
