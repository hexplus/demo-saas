import { Button } from '@/components/ui/button';
import { useContext } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { GlobalContext } from '@/context/GlobalContext';
import { Separator } from '@/components/ui/separator';
import { WandSparkles } from 'lucide-react';
import { Rephrase } from './Rephrase';
import { Summary } from './Summary';
import { Sparkle } from 'lucide-react';
import { toast } from 'sonner';

export function AiSettings() {
  const globalContext = useContext(GlobalContext);

  if (!globalContext) {
    throw new Error('GlobalContext is undefined');
  }

  const {
    ai,
    isProcessing,
    summary,
    rephrase,
    style,
    tone,
    complexity,
    summaryType,
    summaryLength,
    content,
  } = globalContext;

  const handleProcessing = () => {
    if (summary && (!summaryLength || !summaryType)) {
      toast('Configuración requerida', {
        description: 'Revise la configuración e intente de nuevo',
      });
      return;
    }

    if (rephrase && (!style || !tone || !complexity)) {
      toast('Configuración requerida', {
        description: 'Revise la configuración e intente de nuevo',
      });
      return;
    }

    if (summary || rephrase) {
      ai();
    } else {
      toast('Configuración requerida', {
        description: 'Revise la configuración e intente de nuevo',
      });
    }
  };

  return (
    <>
      <div className="flex p-4 justify-center">
        <Button
          disabled={
            isProcessing || (!summary && !rephrase) || content.length == 0
          }
          onClick={handleProcessing}
        >
          {isProcessing ? (
            <>
              <Sparkle className="mr-2 h-4 w-4 animate-spin" />
              Procesando
            </>
          ) : (
            <>
              <WandSparkles className="mr-2 h-4 w-4" />
              Procesar con AI
            </>
          )}
        </Button>
      </div>
      <Separator />

      <ScrollArea className="h-screen">
        <Rephrase />
        <Summary />
        {/* <Seo /> */}
      </ScrollArea>
    </>
  );
}
