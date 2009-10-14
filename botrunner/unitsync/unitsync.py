import os, ctypes
from ctypes import c_bool, c_char, c_char_p, c_int, c_uint, c_float, Structure, create_string_buffer, cast, pointer

class StartPos(Structure):
	_fields_ = [('x', c_int), ('y', c_int)]
	def __str__(self):
		return '(%i, %i)' % (self.x, self.y)

class MapInfo(Structure):
	def __init__(self):
		self.author = cast(create_string_buffer(200), c_char_p) # BUG: author field shows up as empty, probably something to do with the fact it's after the startpos structs
		self.description = cast(create_string_buffer(255), c_char_p)
		
	_fields_ = [('description', c_char_p),
			('tidalStrength', c_int),
			('gravity', c_int),
			('maxMetal', c_float),
			('extractorRadius', c_int),
			('minWind', c_int),
			('maxWind', c_int),
			('width', c_int),
			('height', c_int),
			('posCount', c_int),
			('StartPos', StartPos * 16),
			('author', c_char_p)]

class Unitsync:
	def __init__(self, location='.'):
		if location.endswith('.so'):
			self.unitsync = ctypes.cdll.LoadLibrary(location)
		elif location.endswith('.dll'): 
			locationdir = os.path.dirname(location)
			# load devil first, to avoid dll conflicts
			ctypes.windll.LoadLibrary(locationdir + "/devil.dll" )
			self.unitsync = ctypes.windll.LoadLibrary(location)

	def GetNextError(self): return c_char_p(self.unitsync.GetNextError()).value
	def GetSpringVersion(self): return c_char_p(self.unitsync.GetSpringVersion()).value
	def Init(self, isServer, id): return c_int(self.unitsync.Init(isServer, id)).value
	def UnInit(self): return (self.unitsync.UnInit()).value
	def GetWritableDataDirectory(self): return c_char_p(self.unitsync.GetWritableDataDirectory()).value
	def ProcessUnits(self): return c_int(self.unitsync.ProcessUnits()).value
	def ProcessUnitsNoChecksum(self): return c_int(self.unitsync.ProcessUnitsNoChecksum()).value
	def GetUnitCount(self): return c_int(self.unitsync.GetUnitCount()).value
	def GetUnitName(self, unit): return c_char_p(self.unitsync.GetUnitName(unit)).value
	def GetFullUnitName(self, unit): return c_char_p(self.unitsync.GetFullUnitName(unit)).value
	def AddArchive(self, name): return (self.unitsync.AddArchive(name)).value
	def AddAllArchives(self, root): return (self.unitsync.AddAllArchives(root)).value
	def RemoveAllArchives(self): return (self.unitsync.RemoveAllArchives()).value
	def GetArchiveChecksum(self, arname): return c_uint(self.unitsync.GetArchiveChecksum(arname)).value
	def GetArchivePath(self, arname): return c_char_p(self.unitsync.GetArchivePath(arname)).value
	def GetMapCount(self): return c_int(self.unitsync.GetMapCount()).value
	def GetMapName(self, index): return c_char_p(self.unitsync.GetMapName(index)).value
	def GetMapInfoEx(self, name, outInfo, version): return c_int(self.unitsync.GetMapInfoEx(name, pointer(outInfo), version)).value
	def GetMapInfo(self, name, outInfo): return c_int(self.unitsync.GetMapInfo(name, pointer(outInfo))).value
	def GetMapMinHeight(self, name): return c_float(self.unitsync.GetMapMinHeight(name)).value
	def GetMapMaxHeight(self, name): return c_float(self.unitsync.GetMapMaxHeight(name)).value
	def GetMapArchiveCount(self, mapName): return c_int(self.unitsync.GetMapArchiveCount(mapName)).value
	def GetMapArchiveName(self, index): return c_char_p(self.unitsync.GetMapArchiveName(index)).value
	def GetMapChecksum(self, index): return c_uint(self.unitsync.GetMapChecksum(index)).value
	def GetMapChecksumFromName(self, mapName): return c_uint(self.unitsync.GetMapChecksumFromName(mapName)).value
	def GetMinimap(self, filename, miplevel): return c_char_p(self.unitsync.GetMinimap(filename, miplevel)).value
	def GetInfoMapSize(self, filename, name, width, height): return c_int(self.unitsync.GetInfoMapSize(filename, name, width, height)).value
	def GetInfoMap(self, filename, name, data, typeHint): return c_int(self.unitsync.GetInfoMap(filename, name, data, typeHint)).value
	def GetSkirmishAICount(self): return c_int(self.unitsync.GetSkirmishAICount()).value
	def GetSkirmishAIInfoCount(self, index): return c_int(self.unitsync.GetSkirmishAIInfoCount(index)).value
	def GetInfoKey(self, index): return c_char_p(self.unitsync.GetInfoKey(index)).value
	def GetInfoValue(self, index): return c_char_p(self.unitsync.GetInfoValue(index)).value
	def GetInfoDescription(self, index): return c_char_p(self.unitsync.GetInfoDescription(index)).value
	def GetSkirmishAIOptionCount(self, index): return c_int(self.unitsync.GetSkirmishAIOptionCount(index)).value
	def GetPrimaryModCount(self): return c_int(self.unitsync.GetPrimaryModCount()).value
	def GetPrimaryModName(self, index): return c_char_p(self.unitsync.GetPrimaryModName(index)).value
	def GetPrimaryModShortName(self, index): return c_char_p(self.unitsync.GetPrimaryModShortName(index)).value
	def GetPrimaryModVersion(self, index): return c_char_p(self.unitsync.GetPrimaryModVersion(index)).value
	def GetPrimaryModMutator(self, index): return c_char_p(self.unitsync.GetPrimaryModMutator(index)).value
	def GetPrimaryModGame(self, index): return c_char_p(self.unitsync.GetPrimaryModGame(index)).value
	def GetPrimaryModShortGame(self, index): return c_char_p(self.unitsync.GetPrimaryModShortGame(index)).value
	def GetPrimaryModDescription(self, index): return c_char_p(self.unitsync.GetPrimaryModDescription(index)).value
	def GetPrimaryModArchive(self, index): return c_char_p(self.unitsync.GetPrimaryModArchive(index)).value
	def GetPrimaryModArchiveCount(self, index): return c_int(self.unitsync.GetPrimaryModArchiveCount(index)).value
	def GetPrimaryModArchiveList(self, arnr): return c_char_p(self.unitsync.GetPrimaryModArchiveList(arnr)).value
	def GetPrimaryModIndex(self, name): return c_int(self.unitsync.GetPrimaryModIndex(name)).value
	def GetPrimaryModChecksum(self, index): return c_uint(self.unitsync.GetPrimaryModChecksum(index)).value
	def GetPrimaryModChecksumFromName(self, name): return c_uint(self.unitsync.GetPrimaryModChecksumFromName(name)).value
	def GetSideCount(self): return c_int(self.unitsync.GetSideCount()).value
	def GetSideName(self, side): return c_char_p(self.unitsync.GetSideName(side)).value
	def GetSideStartUnit(self, side): return c_char_p(self.unitsync.GetSideStartUnit(side)).value
	def GetMapOptionCount(self, name): return c_int(self.unitsync.GetMapOptionCount(name)).value
	def GetModOptionCount(self): return c_int(self.unitsync.GetModOptionCount()).value
	def GetCustomOptionCount(self, filename): return c_int(self.unitsync.GetCustomOptionCount(filename)).value
	def GetOptionKey(self, optIndex): return c_char_p(self.unitsync.GetOptionKey(optIndex)).value
	def GetOptionScope(self, optIndex): return c_char_p(self.unitsync.GetOptionScope(optIndex)).value
	def GetOptionName(self, optIndex): return c_char_p(self.unitsync.GetOptionName(optIndex)).value
	def GetOptionSection(self, optIndex): return c_char_p(self.unitsync.GetOptionSection(optIndex)).value
	def GetOptionStyle(self, optIndex): return c_char_p(self.unitsync.GetOptionStyle(optIndex)).value
	def GetOptionDesc(self, optIndex): return c_char_p(self.unitsync.GetOptionDesc(optIndex)).value
	def GetOptionType(self, optIndex): return c_int(self.unitsync.GetOptionType(optIndex)).value
	def GetOptionBoolDef(self, optIndex): return c_int(self.unitsync.GetOptionBoolDef(optIndex)).value
	def GetOptionNumberDef(self, optIndex): return c_float(self.unitsync.GetOptionNumberDef(optIndex)).value
	def GetOptionNumberMin(self, optIndex): return c_float(self.unitsync.GetOptionNumberMin(optIndex)).value
	def GetOptionNumberMax(self, optIndex): return c_float(self.unitsync.GetOptionNumberMax(optIndex)).value
	def GetOptionNumberStep(self, optIndex): return c_float(self.unitsync.GetOptionNumberStep(optIndex)).value
	def GetOptionStringDef(self, optIndex): return c_char_p(self.unitsync.GetOptionStringDef(optIndex)).value
	def GetOptionStringMaxLen(self, optIndex): return c_int(self.unitsync.GetOptionStringMaxLen(optIndex)).value
	def GetOptionListCount(self, optIndex): return c_int(self.unitsync.GetOptionListCount(optIndex)).value
	def GetOptionListDef(self, optIndex): return c_char_p(self.unitsync.GetOptionListDef(optIndex)).value
	def GetOptionListItemKey(self, optIndex, itemIndex): return c_char_p(self.unitsync.GetOptionListItemKey(optIndex, itemIndex)).value
	def GetOptionListItemName(self, optIndex, itemIndex): return c_char_p(self.unitsync.GetOptionListItemName(optIndex, itemIndex)).value
	def GetOptionListItemDesc(self, optIndex, itemIndex): return c_char_p(self.unitsync.GetOptionListItemDesc(optIndex, itemIndex)).value
	def GetModValidMapCount(self): return c_int(self.unitsync.GetModValidMapCount()).value
	def GetModValidMap(self, index): return c_char_p(self.unitsync.GetModValidMap(index)).value
	def OpenFileVFS(self, name): return c_int(self.unitsync.OpenFileVFS(name)).value
	def CloseFileVFS(self, handle): return (self.unitsync.CloseFileVFS(handle)).value
	def ReadFileVFS(self, handle, buf, length): return c_int(self.unitsync.ReadFileVFS(handle, buf, length)).value
	def FileSizeVFS(self, handle): return c_int(self.unitsync.FileSizeVFS(handle)).value
	def InitFindVFS(self, pattern): return c_int(self.unitsync.InitFindVFS(pattern)).value
	def InitDirListVFS(self, path, pattern, modes): return c_int(self.unitsync.InitDirListVFS(path, pattern, modes)).value
	def InitSubDirsVFS(self, path, pattern, modes): return c_int(self.unitsync.InitSubDirsVFS(path, pattern, modes)).value
	def FindFilesVFS(self, handle, nameBuf, size): return c_int(self.unitsync.FindFilesVFS(handle, nameBuf, size)).value
	def OpenArchive(self, name): return c_int(self.unitsync.OpenArchive(name)).value
	def OpenArchiveType(self, name, type): return c_int(self.unitsync.OpenArchiveType(name, type)).value
	def CloseArchive(self, archive): return (self.unitsync.CloseArchive(archive)).value
	def FindFilesArchive(self, archive, cur, nameBuf, size): return c_int(self.unitsync.FindFilesArchive(archive, cur, nameBuf, size)).value
	def OpenArchiveFile(self, archive, name): return c_int(self.unitsync.OpenArchiveFile(archive, name)).value
	def ReadArchiveFile(self, archive, handle, buffer, numBytes): return c_int(self.unitsync.ReadArchiveFile(archive, handle, buffer, numBytes)).value
	def CloseArchiveFile(self, archive, handle): return (self.unitsync.CloseArchiveFile(archive, handle)).value
	def SizeArchiveFile(self, archive, handle): return c_int(self.unitsync.SizeArchiveFile(archive, handle)).value
	def SetSpringConfigFile(self, filenameAsAbsolutePath): return (self.unitsync.SetSpringConfigFile(filenameAsAbsolutePath)).value
	def GetSpringConfigFile(self): return c_char_p(self.unitsync.GetSpringConfigFile()).value
	def GetSpringConfigString(self, name, defvalue): return c_char_p(self.unitsync.GetSpringConfigString(name, defvalue)).value
	def GetSpringConfigInt(self, name, defvalue): return c_int(self.unitsync.GetSpringConfigInt(name, defvalue)).value
	def GetSpringConfigFloat(self, name, defvalue): return c_float(self.unitsync.GetSpringConfigFloat(name, defvalue)).value
	def SetSpringConfigString(self, name, value): return (self.unitsync.SetSpringConfigString(name, value)).value
	def SetSpringConfigInt(self, name, value): return (self.unitsync.SetSpringConfigInt(name, value)).value
	def SetSpringConfigFloat(self, name, value): return (self.unitsync.SetSpringConfigFloat(name, value)).value
	def lpClose(self): return (self.unitsync.lpClose()).value
	def lpOpenFile(self, filename, fileModes, accessModes): return c_int(self.unitsync.lpOpenFile(filename, fileModes, accessModes)).value
	def lpOpenSource(self, source, accessModes): return c_int(self.unitsync.lpOpenSource(source, accessModes)).value
	def lpExecute(self): return c_int(self.unitsync.lpExecute()).value
	def lpErrorLog(self): return c_char_p(self.unitsync.lpErrorLog()).value
	def lpAddTableInt(self, key, override): return (self.unitsync.lpAddTableInt(key, override)).value
	def lpAddTableStr(self, key, override): return (self.unitsync.lpAddTableStr(key, override)).value
	def lpEndTable(self): return (self.unitsync.lpEndTable()).value
	def lpAddIntKeyIntVal(self, key, val): return (self.unitsync.lpAddIntKeyIntVal(key, val)).value
	def lpAddStrKeyIntVal(self, key, val): return (self.unitsync.lpAddStrKeyIntVal(key, val)).value
	def lpAddIntKeyBoolVal(self, key, val): return (self.unitsync.lpAddIntKeyBoolVal(key, val)).value
	def lpAddStrKeyBoolVal(self, key, val): return (self.unitsync.lpAddStrKeyBoolVal(key, val)).value
	def lpAddIntKeyFloatVal(self, key, val): return (self.unitsync.lpAddIntKeyFloatVal(key, val)).value
	def lpAddStrKeyFloatVal(self, key, val): return (self.unitsync.lpAddStrKeyFloatVal(key, val)).value
	def lpAddIntKeyStrVal(self, key, val): return (self.unitsync.lpAddIntKeyStrVal(key, val)).value
	def lpAddStrKeyStrVal(self, key, val): return (self.unitsync.lpAddStrKeyStrVal(key, val)).value
	def lpRootTable(self): return c_int(self.unitsync.lpRootTable()).value
	def lpRootTableExpr(self, expr): return c_int(self.unitsync.lpRootTableExpr(expr)).value
	def lpSubTableInt(self, key): return c_int(self.unitsync.lpSubTableInt(key)).value
	def lpSubTableStr(self, key): return c_int(self.unitsync.lpSubTableStr(key)).value
	def lpSubTableExpr(self, expr): return c_int(self.unitsync.lpSubTableExpr(expr)).value
	def lpPopTable(self): return (self.unitsync.lpPopTable()).value
	def lpGetKeyExistsInt(self, key): return c_int(self.unitsync.lpGetKeyExistsInt(key)).value
	def lpGetKeyExistsStr(self, key): return c_int(self.unitsync.lpGetKeyExistsStr(key)).value
	def lpGetIntKeyType(self, key): return c_int(self.unitsync.lpGetIntKeyType(key)).value
	def lpGetStrKeyType(self, key): return c_int(self.unitsync.lpGetStrKeyType(key)).value
	def lpGetIntKeyListCount(self): return c_int(self.unitsync.lpGetIntKeyListCount()).value
	def lpGetIntKeyListEntry(self, index): return c_int(self.unitsync.lpGetIntKeyListEntry(index)).value
	def lpGetStrKeyListCount(self): return c_int(self.unitsync.lpGetStrKeyListCount()).value
	def lpGetStrKeyListEntry(self, index): return c_char_p(self.unitsync.lpGetStrKeyListEntry(index)).value
	def lpGetIntKeyIntVal(self, key, defVal): return c_int(self.unitsync.lpGetIntKeyIntVal(key, defVal)).value
	def lpGetStrKeyIntVal(self, key, defVal): return c_int(self.unitsync.lpGetStrKeyIntVal(key, defVal)).value
	def lpGetIntKeyBoolVal(self, key, defVal): return c_int(self.unitsync.lpGetIntKeyBoolVal(key, defVal)).value
	def lpGetStrKeyBoolVal(self, key, defVal): return c_int(self.unitsync.lpGetStrKeyBoolVal(key, defVal)).value
	def lpGetIntKeyFloatVal(self, key, defVal): return c_float(self.unitsync.lpGetIntKeyFloatVal(key, defVal)).value
	def lpGetStrKeyFloatVal(self, key, defVal): return c_float(self.unitsync.lpGetStrKeyFloatVal(key, defVal)).value
	def lpGetIntKeyStrVal(self, key, defVal): return c_char_p(self.unitsync.lpGetIntKeyStrVal(key, defVal)).value
	def lpGetStrKeyStrVal(self, key, defVal): return c_char_p(self.unitsync.lpGetStrKeyStrVal(key, defVal)).value