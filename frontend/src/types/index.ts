export interface Organization {
  id: string;
  name: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  status: string;
}

export interface Task {
  id: string;
  title: string;
  status: string;
}
