import { useQuery } from "@apollo/client/react";
import { GET_PROJECTS } from "../graphql/queries";
import { GetProjectsResponse } from "../types/graphql";

export default function ProjectList() {
  const { data, loading, error } = useQuery<GetProjectsResponse>(GET_PROJECTS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  if (!data) return null;

  return (
    <div>
      {data.projects.map((project) => (
        <div key={project.id}>
          <h3>{project.name}</h3>
          <p>Status: {project.status}</p>
        </div>
      ))}
    </div>
  );
}
