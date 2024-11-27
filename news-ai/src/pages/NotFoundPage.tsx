import { Outlet } from 'react-router-dom';

const NotFoundPage = () => (
  <div>
    <main>
      <Outlet />
    </main>
  </div>
);

export default NotFoundPage;
