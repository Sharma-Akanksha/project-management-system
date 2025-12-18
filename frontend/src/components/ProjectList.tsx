// import { useQuery } from "@apollo/client/react";
// import { GET_PROJECTS } from "../graphql/queries";
// import { GetProjectsResponse } from "../types/graphql";

// export default function ProjectList() {
//   const { data, loading, error } = useQuery<GetProjectsResponse>(GET_PROJECTS);

//   if (loading) return <p>Loading...</p>;
//   if (error) return <p>Error: {error.message}</p>;
//   if (!data) return null;

//   return (
//     <div>
//       {data.projects.map((project) => (
//         <div key={project.id}>
//           <h3>{project.name}</h3>
//           <p>Status: {project.status}</p>
//         </div>
//       ))}
//     </div>
//   );
// }

import { useQuery } from "@apollo/client/react";
import { GET_PROJECTS } from "../graphql/queries";
import { GetProjectsResponse } from "../types/graphql";

interface ProjectListProps {
  organizationSlug: string;
}

const ProjectList = ({ organizationSlug }: ProjectListProps) => {
    const { data, loading, error } = useQuery<GetProjectsResponse>(GET_PROJECTS, {
    variables: { organizationSlug },});
    if (loading) return <p>Loading projects...</p>;
    if (error) return <p>Error: {error.message}</p>;
    if (!data) return null;

    return (
        <div className="grid gap-4">
            {data.projects.map((project: any) => (
                <div
                key={project.id}
                className="bg-white p-4 rounded shadow"
                >
                <h2 className="text-lg font-semibold">{project.name}</h2>
                <p>Total Tasks: {project.taskCount}</p>
                <p>Completed: {project.completedTasks}</p>
                <p>Completion Rate: {project.completionRate}%</p>
                </div>
            ))}
        </div>
    );
};

export default ProjectList;

