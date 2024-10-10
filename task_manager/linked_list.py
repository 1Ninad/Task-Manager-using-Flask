# linked_list.py
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, task):
        new_node = Node(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, task_id):
        if not self.head:
            return False
        # Handle deletion of head node
        if self.head.task.id == task_id:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if current.next.task.id == task_id:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def get_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.task)
            current = current.next
        return tasks
