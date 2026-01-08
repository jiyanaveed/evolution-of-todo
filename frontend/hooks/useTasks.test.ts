import { renderHook, act, waitFor } from '@testing-library/react';
import useTasks from './useTasks';
import * as taskApi from '../lib/task-api';

// Mock the taskApi module
jest.mock('../lib/task-api');

const mockTaskApi = taskApi as jest.Mocked<typeof taskApi>;

describe('useTasks', () => {
  const mockTask = {
    id: 1,
    title: 'Test task',
    completed: false,
  };

  const mockCreateTaskRequest = {
    title: 'New task',
  };

  const mockUpdateTaskRequest = {
    title: 'Updated task',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('initially loads tasks and sets loading state', async () => {
    mockTaskApi.getTasks.mockResolvedValue([mockTask]);

    let result: any;
    await act(async () => {
      const { result: hookResult } = renderHook(() => useTasks());
      result = hookResult;
      // Wait for the async effect to complete
      await waitFor(() => expect(result.current.loading).toBe(false));
    });

    expect(mockTaskApi.getTasks).toHaveBeenCalledTimes(1);
    expect(result.current.tasks).toEqual([mockTask]);
    expect(result.current.loading).toBe(false);
  });

  it('handles error when fetching tasks fails', async () => {
    mockTaskApi.getTasks.mockRejectedValue(new Error('Failed to fetch'));

    let result: any;
    await act(async () => {
      const { result: hookResult } = renderHook(() => useTasks());
      result = hookResult;
      await waitFor(() => expect(result.current.loading).toBe(false));
    });

    expect(result.current.error).toBe('Failed to fetch tasks');
  });

  it('creates a new task', async () => {
    mockTaskApi.createTask.mockResolvedValue({
      id: 2,
      title: 'New task',
      completed: false,
    });

    let result: any;
    await act(async () => {
      const { result: hookResult } = renderHook(() => useTasks());
      result = hookResult;
      // Wait for initial fetch to complete
      await waitFor(() => expect(result.current.loading).toBe(false));
    });

    await act(async () => {
      result.current.createTask(mockCreateTaskRequest);
    });

    await waitFor(() => {
      expect(mockTaskApi.createTask).toHaveBeenCalledWith(mockCreateTaskRequest);
      expect(result.current.tasks).toContainEqual({
        id: 2,
        title: 'New task',
        completed: false,
      });
    });
  });

  it('updates an existing task', async () => {
    mockTaskApi.getTasks.mockResolvedValue([mockTask]);
    mockTaskApi.updateTask.mockResolvedValue({
      ...mockTask,
      title: 'Updated task',
    });

    let result: any;
    await act(async () => {
      const { result: hookResult } = renderHook(() => useTasks());
      result = hookResult;
      await waitFor(() => expect(result.current.loading).toBe(false));
    });

    await act(async () => {
      result.current.updateTask(1, mockUpdateTaskRequest);
    });

    await waitFor(() => {
      expect(mockTaskApi.updateTask).toHaveBeenCalledWith(1, mockUpdateTaskRequest);
      expect(result.current.tasks).toContainEqual({
        id: 1,
        title: 'Updated task',
        completed: false,
      });
    });
  });

  it('deletes a task', async () => {
    mockTaskApi.getTasks.mockResolvedValue([mockTask, { id: 2, title: 'Another task', completed: false }]);
    mockTaskApi.deleteTask.mockResolvedValue();

    let result: any;
    await act(async () => {
      const { result: hookResult } = renderHook(() => useTasks());
      result = hookResult;
      await waitFor(() => expect(result.current.loading).toBe(false));
    });

    const initialTasksLength = result.current.tasks.length;

    await act(async () => {
      result.current.deleteTask(1);
    });

    await waitFor(() => {
      expect(mockTaskApi.deleteTask).toHaveBeenCalledWith(1);
      expect(result.current.tasks).toHaveLength(initialTasksLength - 1);
      expect(result.current.tasks).not.toContainEqual(mockTask);
    });
  });

  it('toggles task completion', async () => {
    mockTaskApi.getTasks.mockResolvedValue([mockTask]);
    mockTaskApi.toggleTaskCompletion.mockResolvedValue({
      ...mockTask,
      completed: true,
    });

    let result: any;
    await act(async () => {
      const { result: hookResult } = renderHook(() => useTasks());
      result = hookResult;
      await waitFor(() => expect(result.current.loading).toBe(false));
    });

    await act(async () => {
      result.current.toggleTaskCompletion(1);
    });

    await waitFor(() => {
      expect(mockTaskApi.toggleTaskCompletion).toHaveBeenCalledWith(1);
      expect(result.current.tasks).toContainEqual({
        id: 1,
        title: 'Test task',
        completed: true,
      });
    });
  });

  it('sets error when task creation fails', async () => {
    mockTaskApi.getTasks.mockResolvedValue([]);
    mockTaskApi.createTask.mockRejectedValue(new Error('Failed to create'));

    let result: any;
    await act(async () => {
      const { result: hookResult } = renderHook(() => useTasks());
      result = hookResult;
      await waitFor(() => expect(result.current.loading).toBe(false));
    });

    await act(async () => {
      result.current.createTask(mockCreateTaskRequest);
    });

    await waitFor(() => {
      expect(result.current.error).toBe('Failed to create task');
    });
  });
});