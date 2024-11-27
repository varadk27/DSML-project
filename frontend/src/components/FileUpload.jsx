import React from 'react';
import { useDropzone } from 'react-dropzone';
import { FileText, Upload } from 'lucide-react';

const FileUpload = ({ onFileSelect }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: acceptedFiles => onFileSelect(acceptedFiles[0]),
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center">
        {isDragActive ? (
          <Upload className="h-12 w-12 text-blue-500 mb-4" />
        ) : (
          <FileText className="h-12 w-12 text-gray-400 mb-4" />
        )}
        <p className="text-gray-600">
          {isDragActive
            ? 'Drop your resume here...'
            : 'Drag & drop your resume PDF here, or click to select'}
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Supports PDF files up to 5MB
        </p>
      </div>
    </div>
  );
};

export default FileUpload;