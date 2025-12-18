import { createContext, useContext } from "react";

interface OrganizationContextType {
  organizationSlug: string;
}

const OrganizationContext = createContext<OrganizationContextType | null>(null);

export const OrganizationProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  // temporary value — later comes from auth / subdomain
  const organizationSlug = "test-org";

  return (
    <OrganizationContext.Provider value={{ organizationSlug }}>
      {children}
    </OrganizationContext.Provider>
  );
};

export const useOrganization = () => {
  const context = useContext(OrganizationContext);
  if (!context) {
    throw new Error("useOrganization must be used within OrganizationProvider");
  }
  return context;
};
