import axios from 'axios';
import taskApi from './task-api';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('taskApi', () => {
  const mockTask = {
    id: 1,
    title: 'Test task',
    completed: false,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getTasks', () => {
    it('fetches tasks successfully', async () => {
      mockedAxios.get.mockResolvedValue({ data: [mockTask] });

      const result = await taskApi.getTasks();

      expect(mockedAxios.get).toHaveBeenCalledWith('/tasks');
      expect(result).toEqual([mockTask]);
    });

    it('handles error when fetching tasks fails', async () => {
      mockedAxios.get.mockRejectedValue(new Error('Network error'));

      await expect(taskApi.getTasks()).rejects.toThrow('Network error');
    });
  });

  describe('getTask', () => {
    it('fetches a single task successfully', async () => {
      mockedAxios.get.mockResolvedValue({ data: mockTask });

      const result = await taskApi.getTask(1);

      expect(mockedAxios.get).toHaveBeenCalledWith('/tasks/1');
      expect(result).toEqual(mockTask);
    });
  });

  describe('createTask', () => {
    it('creates a task successfully', async () => {
      const newTask = { ...mockTask, id: 2 };
      const taskData = { title: 'New task' };

      mockedAxios.post.mockResolvedValue({ data: newTask });

      const result = await taskApi.createTask(taskData);

      expect(mockedAxios.post).toHaveBeenCalledWith('/tasks', taskData);
      expect(result).toEqual(newTask);
    });
  });

  describe('updateTask', () => {
    it('updates a task successfully', async () => {
      const updatedTask = { ...mockTask, title: 'Updated task' };
      const taskData = { title: 'Updated task' };

      mockedAxios.put.mockResolvedValue({ data: updatedTask });

      const result = await taskApi.updateTask(1, taskData);

      expect(mockedAxios.put).toHaveBeenCalledWith('/tasks/1', taskData);
      expect(result).toEqual(updatedTask);
    });
  });

  describe('deleteTask', () => {
    it('deletes a task successfully', async () => {
      mockedAxios.delete.mockResolvedValue({});

      await taskApi.deleteTask(1);

      expect(mockedAxios.delete).toHaveBeenCalledWith('/tasks/1');
    });
  });

  describe('toggleTaskCompletion', () => {
    it('toggles task completion successfully', async () => {
      const completedTask = { ...mockTask, completed: true };

      mockedAxios.patch.mockResolvedValue({ data: completedTask });

      const result = await taskApi.toggleTaskCompletion(1);

      expect(mockedAxios.patch).toHaveBeenCalledWith('/tasks/1/complete');
      expect(result).toEqual(completedTask);
    });
  });
});