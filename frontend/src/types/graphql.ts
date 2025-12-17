export interface Project {
  id: string;
  name: string;
  status: string;
}

export interface GetProjectsResponse {
  projects: Project[];
}