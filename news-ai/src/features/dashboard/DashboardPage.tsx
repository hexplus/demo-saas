import { News } from '@/components/News';
import { Header } from '@/components/Header/Header';
import { useEffect, useState, useContext } from 'react';
import { fetchData } from '@/services/api';
import { GlobalContext } from '@/context/GlobalContext';
import { Toaster } from '@/components/ui/sonner';

export default function DashboardPage() {
  // const layout = cookies().get('react-resizable-panels:layout:adapter');
  // const collapsed = cookies().get('react-resizable-panels:collapsed');
  //const defaultLayout = layout ? JSON.parse(layout.value) : undefined
  // const defaultCollapsed = collapsed ? JSON.parse(collapsed.value) : undefined

  const defaultLayout = [];
  const defaultCollapsed = false;
  const [error, setError] = useState('');
  // const [adapters, setAdapters] = useState([]);
  const headlines = [];

  const context = useContext(GlobalContext);
  const { adapterLanguage, setAdapters, adapters } = context;

  useEffect(() => {
    const loadAdapters = async () => {
      try {
        const result = await fetchData('/adapters');
        setAdapters(result.adapters);
      } catch (err) {
        setError('Error loading data');
      }
    };

    loadAdapters();
  }, []);

  return (
    <>
      <Header />
      <div className="flex-col md:flex">
        <News
          adapters={adapters}
          headlines={headlines}
          defaultLayout={defaultLayout}
          defaultCollapsed={defaultCollapsed}
          navCollapsedSize={4}
        />
      </div>
      <Toaster />
    </>
  );
}
