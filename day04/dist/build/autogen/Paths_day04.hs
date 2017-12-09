module Paths_day04 (
    version,
    getBinDir, getLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
catchIO = Exception.catch

version :: Version
version = Version [0,1,0,0] []
bindir, libdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/home/nalderso/.cabal/bin"
libdir     = "/home/nalderso/.cabal/lib/x86_64-linux-ghc-7.10.3/day04-0.1.0.0-1jtEWYN8mgxElI73FN7Tdh"
datadir    = "/home/nalderso/.cabal/share/x86_64-linux-ghc-7.10.3/day04-0.1.0.0"
libexecdir = "/home/nalderso/.cabal/libexec"
sysconfdir = "/home/nalderso/.cabal/etc"

getBinDir, getLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "day04_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "day04_libdir") (\_ -> return libdir)
getDataDir = catchIO (getEnv "day04_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "day04_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "day04_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
