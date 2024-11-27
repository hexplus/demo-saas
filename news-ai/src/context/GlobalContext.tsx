import { createContext, useReducer, ReactNode } from 'react';
import { User } from '../types/User';
import { postData, fetchData } from '../services/api';
import { useNavigate } from 'react-router-dom';

interface GlobalProviderProps {
  children: ReactNode;
}

interface Content {
  title: string;
  content: string;
}

interface GlobalState {
  user: User | null;
  adapter: string;
  adapterLanguage: string;
  adapters: any[];
  headlines: any[];
  categories: any[];
  content: Content[];
  editorContent: any[];
  styles: any[];
  tones: any[];
  complexities: any[];
  summaryTypes: any[];
  summaryLengths: any[];
  style: string;
  tone: string;
  complexity: string;
  rephrase: boolean;
  summary: boolean;
  summaryType: string;
  summaryLength: string;
  isLoadingHeadlines: boolean;
  isLoadingCategories: boolean;
  isLoadingContent: boolean;
  isLoadingStyles: boolean;
  isLoadingTones: boolean;
  isLoadingComplexities: boolean;
  isLoadingSummaryTypes: boolean;
  isLoadingSummaryLengths: boolean;
  isProcessing: boolean;
}

interface GlobalContextType {
  user: User | null;
  setUser: (user: User) => void;
  ai: () => Promise<void>;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  adapter: string;
  adapterLanguage: string;
  setAdapter: (adapter: string) => void;
  setAdapters: (adapters: any[]) => void;
  setTone: (value: string) => void;
  setStyle: (value: string) => void;
  setComplexity: (value: string) => void;
  setSummaryLengths: (value: string[]) => void;
  setRephrase: (value: boolean) => void;
  setSummary: (value: boolean) => void;
  setSummaryType: (value: string) => void;
  setSummaryLength: (value: string) => void;
  setAdapterLanguage: (language: string) => void;
  setEditorContent: (content: string[]) => void;
  fetchHeadlines: (adapterCode: string, slug?: string) => Promise<void>;
  fetchCategories: (adapterCode: string) => Promise<void>;
  fetchContent: (adapterCode: string, slug: string) => Promise<void>;
  fetchStyles: () => Promise<void>;
  fetchTones: () => Promise<void>;
  fetchComplexities: () => Promise<void>;
  fetchSummaryTypes: () => Promise<void>;
  fetchSummaryLengths: () => Promise<void>;
  duplicateContent: () => void;
  headlines: any[];
  adapters: any[];
  categories: any[];
  content: Content[];
  editorContent: any[];
  styles: any[];
  tones: any[];
  complexities: any[];
  summaryLengths: any[];
  summaryTypes: any[];
  tone: string;
  style: string;
  complexity: string;
  rephrase: boolean;
  summary: boolean;
  summaryType: string;
  summaryLength: string;
  isLoadingHeadlines: boolean;
  isLoadingCategories: boolean;
  isLoadingContent: boolean;
  isLoadingStyles: boolean;
  isLoadingTones: boolean;
  isLoadingComplexities: boolean;
  isLoadingSummaryLengths: boolean;
  isLoadingSummaryTypes: boolean;
  isProcessing: boolean;
}

type Action =
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'SET_ADAPTER'; payload: string }
  | { type: 'SET_ADAPTERS'; payload: any[] }
  | { type: 'SET_STYLE'; payload: string }
  | { type: 'SET_TONE'; payload: string }
  | { type: 'SET_COMPLEXITY'; payload: string }
  | { type: 'SET_SUMMARY_TYPE'; payload: string }
  | { type: 'SET_SUMMARY_LENGTH'; payload: string }
  | { type: 'SET_ADAPTER_LANGUAGE'; payload: string }
  | { type: 'SET_HEADLINES'; payload: any[] }
  | { type: 'SET_CATEGORIES'; payload: any[] }
  | { type: 'SET_CONTENT'; payload: Content[] }
  | { type: 'SET_EDITOR_CONTENT'; payload: any[] }
  | { type: 'SET_STYLES'; payload: any[] }
  | { type: 'SET_TONES'; payload: any[] }
  | { type: 'SET_COMPLEXITIES'; payload: any[] }
  | { type: 'SET_SUMMARY_TYPES'; payload: any[] }
  | { type: 'SET_SUMMARY_LENGTHS'; payload: any[] }
  | { type: 'SET_REPHRASE'; payload: boolean }
  | { type: 'SET_SUMMARY'; payload: boolean }
  | { type: 'SET_LOADING'; payload: { key: keyof GlobalState; value: boolean } }
  | { type: 'SET_PROCESSING'; payload: boolean }
  | { type: 'LOGOUT' };

const initialState: GlobalState = {
  user: null,
  adapter: '',
  adapterLanguage: 'SPA',
  headlines: [],
  adapters: [],
  categories: [],
  content: [],
  editorContent: [],
  styles: [],
  tones: [],
  complexities: [],
  summaryTypes: [],
  summaryLengths: [],
  style: '',
  tone: '',
  complexity: '',
  summaryType: '',
  summaryLength: '',
  isLoadingHeadlines: false,
  isLoadingCategories: false,
  isLoadingContent: false,
  isLoadingStyles: false,
  isLoadingTones: false,
  isLoadingComplexities: false,
  isLoadingSummaryTypes: false,
  isLoadingSummaryLengths: false,
  isProcessing: false,
  rephrase: false,
  summary: false,
};

const globalReducer = (state: GlobalState, action: Action): GlobalState => {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_ADAPTER':
      return { ...state, adapter: action.payload };
    case 'SET_ADAPTERS':
      return { ...state, adapters: action.payload };
    case 'SET_ADAPTER_LANGUAGE':
      return { ...state, adapterLanguage: action.payload };
    case 'SET_HEADLINES':
      return { ...state, headlines: action.payload };
    case 'SET_CATEGORIES':
      return { ...state, categories: action.payload };
    case 'SET_CONTENT':
      return { ...state, content: action.payload };
    case 'SET_EDITOR_CONTENT':
      return { ...state, editorContent: action.payload };
    case 'SET_STYLES':
      return { ...state, styles: action.payload };
    case 'SET_TONES':
      return { ...state, tones: action.payload };
    case 'SET_COMPLEXITIES':
      return { ...state, complexities: action.payload };
    case 'SET_SUMMARY_TYPES':
      return { ...state, summaryTypes: action.payload };
    case 'SET_SUMMARY_LENGTHS':
      return { ...state, summaryLengths: action.payload };
    case 'SET_LOADING':
      return { ...state, [action.payload.key]: action.payload.value };
    case 'SET_PROCESSING':
      return { ...state, isProcessing: action.payload };
    case 'SET_STYLE':
      return { ...state, style: action.payload };
    case 'SET_TONE':
      return { ...state, tone: action.payload };
    case 'SET_SUMMARY_TYPE':
      return { ...state, summaryType: action.payload };
    case 'SET_SUMMARY_LENGTH':
      return { ...state, summaryLength: action.payload };
    case 'SET_COMPLEXITY':
      return { ...state, complexity: action.payload };
    case 'SET_REPHRASE':
      return { ...state, rephrase: action.payload };
    case 'SET_SUMMARY':
      return { ...state, summary: action.payload };
    case 'LOGOUT':
      return { ...state, user: null };
    default:
      return state;
  }
};

export const GlobalContext = createContext<GlobalContextType | undefined>(
  undefined
);

export const GlobalProvider = ({ children }: GlobalProviderProps) => {
  const [state, dispatch] = useReducer(globalReducer, initialState);
  const navigate = useNavigate();

  const setUser = (user: User) => dispatch({ type: 'SET_USER', payload: user });

  const setAdapter = (adapter: string) =>
    dispatch({ type: 'SET_ADAPTER', payload: adapter });

  const setAdapters = (adapters: any[]) =>
    dispatch({ type: 'SET_ADAPTERS', payload: adapters });

  const setAdapterLanguage = (language: string) =>
    dispatch({ type: 'SET_ADAPTER_LANGUAGE', payload: language });

  const setStyle = (value: string) => {
    dispatch({ type: 'SET_STYLE', payload: value });
  };

  const setTone = (value: string) => {
    dispatch({ type: 'SET_TONE', payload: value });
  };

  const setComplexity = (value: string) => {
    dispatch({ type: 'SET_COMPLEXITY', payload: value });
  };

  const setSummaryLengths = (value: any[]) => {
    dispatch({ type: 'SET_SUMMARY_LENGTHS', payload: value });
  };

  const setRephrase = (value: boolean) => {
    dispatch({ type: 'SET_REPHRASE', payload: value });
  };

  const setSummary = (value: boolean) => {
    dispatch({ type: 'SET_SUMMARY', payload: value });
  };

  const setSummaryType = (value: string) => {
    dispatch({ type: 'SET_SUMMARY_TYPE', payload: value });
  };

  const setSummaryLength = (value: string) => {
    dispatch({ type: 'SET_SUMMARY_LENGTH', payload: value });
  };

  const setEditorContent = (value: string[]) => {
    dispatch({ type: 'SET_EDITOR_CONTENT', payload: value });
  };

  const setLoading = (key: keyof GlobalState, value: boolean) =>
    dispatch({ type: 'SET_LOADING', payload: { key, value } });

  const login = async (username: string, password: string) => {
    try {
      const response = await postData('/login', { username, password });
      dispatch({ type: 'SET_USER', payload: response.user });
      localStorage.setItem('user', JSON.stringify(response.user));
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      navigate('/dashboard');
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  const fetchDataAndDispatch = async (
    url: string,
    actionType: Action['type']
  ) => {
    try {
      const data = await fetchData(url);
      dispatch({ type: actionType, payload: data });
    } catch (error) {
      console.error(`Error fetching ${actionType.toLowerCase()}:`, error);
    }
  };

  const fetchHeadlines = async (adapterCode: string, slug?: string) => {
    setAdapter(adapterCode);
    setLoading('isLoadingHeadlines', true);
    dispatch({ type: 'SET_HEADLINES', payload: [] });
    dispatch({ type: 'SET_CONTENT', payload: [] });
    dispatch({ type: 'SET_EDITOR_CONTENT', payload: [] });
    await fetchDataAndDispatch(
      slug
        ? `/headlines/${adapterCode}?slug=${slug}`
        : `/headlines/${adapterCode}`,
      'SET_HEADLINES'
    );
    setLoading('isLoadingHeadlines', false);
  };

  const fetchCategories = async (adapterCode: string) => {
    dispatch({ type: 'SET_CATEGORIES', payload: [] });
    setLoading('isLoadingCategories', true);
    await fetchDataAndDispatch(`/categories/${adapterCode}`, 'SET_CATEGORIES');
    setLoading('isLoadingCategories', false);
  };

  const fetchContent = async (adapterCode: string, slug: string) => {
    clean();
    setLoading('isLoadingContent', true);
    await fetchDataAndDispatch(
      `/content/${adapterCode}?slug=${slug}`,
      'SET_CONTENT'
    );
    setLoading('isLoadingContent', false);
  };

  const fetchStyles = async () => {
    setLoading('isLoadingStyles', true);
    await fetchDataAndDispatch(`/styles`, 'SET_STYLES');
    setLoading('isLoadingStyles', false);
  };

  const fetchTones = async () => {
    setLoading('isLoadingTones', true);
    await fetchDataAndDispatch(`/tones`, 'SET_TONES');
    setLoading('isLoadingTones', false);
  };

  const fetchComplexities = async () => {
    setLoading('isLoadingComplexities', true);
    await fetchDataAndDispatch(`/complexities`, 'SET_COMPLEXITIES');
    setLoading('isLoadingComplexities', false);
  };

  const fetchSummaryLengths = async () => {
    setLoading('isLoadingSummaryLengths', true);
    await fetchDataAndDispatch(`/summary-lengths`, 'SET_SUMMARY_LENGTHS');
    setLoading('isLoadingSummaryLengths', false);
  };

  const fetchSummaryTypes = async () => {
    setLoading('isLoadingSummaryTypes', true);
    await fetchDataAndDispatch(`/summary-types`, 'SET_SUMMARY_TYPES');
    setLoading('isLoadingSummaryTypes', false);
  };

  const duplicateContent = () => {
    dispatch({ type: 'SET_EDITOR_CONTENT', payload: state.content });
  };

  const logout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    dispatch({ type: 'LOGOUT' });
    navigate('/login');
  };

  const clean = () => {
    dispatch({ type: 'SET_CONTENT', payload: [] });
    dispatch({ type: 'SET_EDITOR_CONTENT', payload: [] });
  };

  const ai = async () => {
    const config = {
      content: state.content,
      rephrase: {
        status: state.rephrase,
        config: {
          style: state.style,
          tone: state.tone,
          complexity: state.complexity,
        },
      },
      summary: {
        status: state.summary,
        config: {
          type: state.summaryType,
          length: state.summaryLength,
        },
      },
    };

    try {
      dispatch({ type: 'SET_EDITOR_CONTENT', payload: [] });
      dispatch({ type: 'SET_PROCESSING', payload: true });
      const editorContent = await postData('/ai', config);
      dispatch({
        type: 'SET_EDITOR_CONTENT',
        payload: editorContent.response,
      });
      dispatch({ type: 'SET_PROCESSING', payload: false });
    } catch (error) {
      dispatch({ type: 'SET_PROCESSING', payload: false });
      console.error('Error fetching AI', error);
    }
  };

  return (
    <GlobalContext.Provider
      value={{
        user: state.user,
        ai,
        setUser,
        login,
        logout,
        adapter: state.adapter,
        adapters: state.adapters,
        style: state.style,
        tone: state.tone,
        complexity: state.complexity,
        summaryType: state.summaryType,
        summaryLength: state.summaryLength,
        adapterLanguage: state.adapterLanguage,
        setAdapter,
        setAdapters,
        setStyle,
        setTone,
        setComplexity,
        setSummaryLengths,
        setRephrase,
        setSummary,
        setSummaryType,
        setSummaryLength,
        setAdapterLanguage,
        setEditorContent,
        fetchHeadlines,
        fetchCategories,
        fetchContent,
        fetchStyles,
        fetchTones,
        fetchComplexities,
        fetchSummaryLengths,
        fetchSummaryTypes,
        duplicateContent,
        headlines: state.headlines,
        categories: state.categories,
        content: state.content,
        editorContent: state.editorContent,
        styles: state.styles,
        tones: state.tones,
        rephrase: state.rephrase,
        summary: state.summary,
        complexities: state.complexities,
        summaryLengths: state.summaryLengths,
        summaryTypes: state.summaryTypes,
        isLoadingHeadlines: state.isLoadingHeadlines,
        isLoadingCategories: state.isLoadingCategories,
        isLoadingContent: state.isLoadingContent,
        isLoadingStyles: state.isLoadingStyles,
        isLoadingTones: state.isLoadingTones,
        isLoadingComplexities: state.isLoadingComplexities,
        isLoadingSummaryLengths: state.isLoadingSummaryLengths,
        isLoadingSummaryTypes: state.isLoadingSummaryTypes,
        isProcessing: state.isProcessing,
      }}
    >
      {children}
    </GlobalContext.Provider>
  );
};
