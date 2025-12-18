import { gql } from "@apollo/client";

export const GET_PROJECTS = gql`
  query GetProjects($organizationSlug: String!) {
    projects(organizationSlug: $organizationSlug) {
      id
      name
      status
      taskCount
      completedTasks
      completionRate
      tasks {
        id
        title
        status
      }
    }
  }
`;
