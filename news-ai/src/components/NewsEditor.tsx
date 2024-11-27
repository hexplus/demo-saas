import { Button } from '@/components/ui/button';
import { GlobalContext } from '@/context/GlobalContext';
import { useContext } from 'react';
import './NewsEditor.scss';

export interface Content {
  text: string;
  type: string;
}

export function NewsEditor() {
  const context = useContext(GlobalContext);
  const { editorContent, setEditorContent } = context;

  const handleCopy = (text: string) => {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        alert('Text copied to clipboard!');
      })
      .catch((err) => {
        console.error('Could not copy text: ', err);
      });
  };

  const fontSizes = ['small', 'medium', 'large', 'huge'];
  const fontFamilies = [
    'Arial',
    'Courier',
    'Georgia',
    'Times New Roman',
    'Verdana',
  ];

  return (
    <div className="flex flex-grow overflow-y-auto flex-col">
      <div className="p-4">
        <form>
          <div className="grid gap-4">
            <div>
              {/* <ReactQuill
                value={editorContent}
                onChange={handleChange}
                placeholder=""
                className="custom-scrollbar"
                theme="snow"
                modules={modules}
                formats={formats}
              /> */}
            </div>
            <div className="flex items-center">
              <Button
                onClick={(e) => e.preventDefault()}
                size="sm"
                className="ml-auto"
              >
                Copiar
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
