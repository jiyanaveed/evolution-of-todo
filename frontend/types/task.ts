export interface Task {
  id: number;
  title: string;
  completed: boolean;
  user_id: string;
}

export interface CreateTaskRequest {
  title: string;
}

export interface UpdateTaskRequest {
  title?: string;
  completed?: boolean;
}

export interface ToggleTaskCompletionRequest {
  completed: boolean;
}

export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface UserCreateRequest {
  email: string;
  password: string;
}

export interface UserLoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}