import ProjectList from "./components/ProjectList";
import { OrganizationProvider } from "./context/OrganizationContext";

function App() {
  const organizationSlug = "test-org";
  return (
    <OrganizationProvider>
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Project Dashboard</h1>
        <ProjectList organizationSlug={organizationSlug} />
      </div>
    </OrganizationProvider>
  );
}

export default App;

