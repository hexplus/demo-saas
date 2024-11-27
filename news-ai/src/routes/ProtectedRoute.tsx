// src/routes/ProtectedRoute.tsx
import { useContext, useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { GlobalContext } from '@/context/GlobalContext';
import { User } from '@/types/User';

interface ProtectedRouteProps {
  children: JSX.Element;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { user } = useContext(GlobalContext);
  const [storedUser, setStoredUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      const localStorageUser = localStorage.getItem('user');
      if (localStorageUser) {
        setStoredUser(JSON.parse(localStorageUser));
      }
    }
    setLoading(false);
  }, [user]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user && !storedUser) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
