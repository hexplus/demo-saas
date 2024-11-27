import { useState, useContext, useEffect } from 'react';
import { Search, CircleAlert } from 'lucide-react';
import { Input } from '@/components/ui/input';
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent } from '@/components/ui/tabs';
import { TooltipProvider } from '@/components/ui/tooltip';
import { AdapterSwitcher } from './AdapterSwitcher';
import { NewsDisplay } from './NewsDisplay';
import { NewsEditor } from './NewsEditor';
import { HeadlinesList } from './HeadlinesList';
import { GlobalContext } from '@/context/GlobalContext';
import './News.scss';
import { CategoriesSwitcher } from './CategoriesSwitcher';
import { AiSettings } from './AiSettings';
import { Switcher } from './Switcher';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface HeadlinesProps {
  adapters: {
    name: string;
    code: string;
    country: string;
    language: string;
    icon: React.ReactNode;
  }[];
  headlines: string[];
  defaultLayout: number[] | undefined;
  defaultCollapsed?: boolean;
  navCollapsedSize: number;
}

export function News({
  adapters,
  headlines,
  defaultLayout = [10, 40, 40, 10],
  defaultCollapsed = false,
}: HeadlinesProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
  const globalContext = useContext(GlobalContext);
  const { categories, content, isProcessing, adapter, editorContent } =
    globalContext;

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  return (
    <TooltipProvider delayDuration={0}>
      <ResizablePanelGroup
        direction="horizontal"
        onLayout={(sizes: number[]) => {
          document.cookie = `react-resizable-panels:layout:mail=${JSON.stringify(
            sizes
          )}`;
        }}
        className="h-full items-stretch custom-height"
      >
        {/* HEALINES LIST */}
        <ResizablePanel
          defaultSize={defaultLayout[0]}
          minSize={20}
          maxSize={20}
        >
          <Tabs defaultValue="all">
            <div className="flex justify-between px-4 py-2 space-x-4">
              <div className="px-0">
                <AdapterSwitcher
                  isCollapsed={isCollapsed}
                  adapters={adapters}
                />
              </div>
              <div>
                <CategoriesSwitcher
                  isCollapsed={isCollapsed}
                  categories={categories ? categories.categories : []}
                />
              </div>
            </div>
            <Separator />
            <div className="bg-background/95 p-4 backdrop-blur supports-[backdrop-filter]:bg-background/60">
              <form>
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Buscar"
                    className="pl-8"
                    disabled={isProcessing}
                  />
                </div>
              </form>
            </div>
            <TabsContent value="all" className="m-0">
              <div className="flex flex-col h-[calc(100vh-168px)]">
                <HeadlinesList items={headlines} />
              </div>
            </TabsContent>
            <TabsContent value="unread" className="m-0">
              <HeadlinesList items={headlines.filter((item) => !item.title)} />
            </TabsContent>
          </Tabs>
        </ResizablePanel>

        <ResizableHandle />

        {/* NEWS PREVIEW */}
        <ResizablePanel defaultSize={defaultLayout[1]} minSize={20}>
          <div className="flex justify-between px-4 py-2 space-x-4 h-[52px]">
            <div className="px-0"></div>
            <div>
              <Button variant="secondary" asChild>
                <a href={content.url} target="_blank" rel="noopener noreferrer">
                  Consultar fuente original
                </a>
              </Button>
            </div>
          </div>
          <Separator />
          <NewsDisplay
            title={content.title}
            content={content.content}
            defaultCollapsed={false}
            complete={false}
          />
        </ResizablePanel>

        <ResizableHandle withHandle />

        {/* EDITOR */}
        <ResizablePanel defaultSize={defaultLayout[2]} minSize={35}>
          <div className="flex justify-between px-4 py-2 space-x-4 h-[80px]">
            <div className="pt-0 text-sm italic">
              <b>Aviso legal:</b> El contenido generado mediante inteligencia
              artificial es un apoyo para facilitar la comprensión y no
              reemplaza ni reproduce el contenido del artículo original. Se
              recomienda consultar el texto completo en su fuente para obtener
              información detallada y precisa..
            </div>
            <div></div>
          </div>
          <Separator />
          <NewsDisplay
            title={editorContent.title}
            content={editorContent.content}
            defaultCollapsed={false}
            complete={true}
          />
        </ResizablePanel>

        <ResizableHandle />

        {/* AI SETTINGS */}
        <ResizablePanel
          defaultSize={defaultLayout[3]}
          minSize={12}
          maxSize={12}
        >
          <AiSettings />
        </ResizablePanel>
      </ResizablePanelGroup>
    </TooltipProvider>
  );
}
