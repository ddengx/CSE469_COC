import maya
timestampFloat = maya.now().epoch
maya_datetime = maya.MayaDT(timestampFloat)
timestampISO8601 = maya_datetime.iso8601().replace('Z', '.0Z')

print(timestampISO8601)
