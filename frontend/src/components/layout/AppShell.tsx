import { NavLink, Outlet } from 'react-router-dom';

export function AppShell() {
  return (
    <>
      <Outlet />
      <nav className="tab-bar">
        <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
          Setup
        </NavLink>
        <NavLink to="/cook" className={({ isActive }) => isActive ? 'active' : ''}>
          Cook
        </NavLink>
        <NavLink to="/report" className={({ isActive }) => isActive ? 'active' : ''}>
          Report
        </NavLink>
      </nav>
    </>
  );
}
